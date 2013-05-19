#!/usr/bin/env python
#-*- coding: utf-8 -*-
import os
import sys
import inspect
import time
import logging


plugin_dir = "plugins"

import plugins.base
import nbCommon

modules = {}


def loadPlugins(plugName):
    """Load plugins from plugin directory"""
    logging.info(u"load module: ==> %s" % plugName)

    try:
        package_obj = __import__(plugin_dir + "." + plugName)
        module_obj = getattr(package_obj, plugName)
        for elem in dir(module_obj):
            obj = getattr(module_obj, elem)
            # Это класс? Класс производный от baseplugin?
            if inspect.isclass(obj) and issubclass(obj, plugins.base.baseplugin):
                # Создаем экземпляр и выполняем функцию run
                modules['object'] = obj()
                return nbCommon.retCodeOK
    except ImportError, e:
        logging.critical(u"Don't load plug. Error: %s" % e)
        return nbCommon.retCodeNoLoadPlug

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print """ USE: python main.py plugNAME
    Where 'plugNAME' - name your plugin from plugins dir.
        """
        exit()

    import ConfigParser
    config = ConfigParser.ConfigParser()
    config.read(nbCommon.iniFile)
    dbgLevel = config.get('main', 'debug_level').lower()
    if dbgLevel == 'debug':
        logging.basicConfig(format=u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s', level=logging.DEBUG)
    elif dbgLevel == 'info':
        logging.basicConfig(format=u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s', level=logging.INFO)
    elif dbgLevel == 'critical':
        logging.basicConfig(format=u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s', level=logging.CRITICAL)
    else:
        logging.basicConfig(format=u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s', level=logging.ERROR)

    err = loadPlugins(sys.argv[1])

    vTimeSleep = nbCommon.vTimeSleep
    while (err[0] == 0) or (err == nbCommon.retCodeNetworkError):
        if err[0] == 0:
            if not os.path.exists('nothing.load'):
                f = open('nothing.load', "w")
                modules['object'].LoadConfig()
                f.close()

            err = modules['object'].getPage()
            err = modules['object'].analysePage(err)

            if err == nbCommon.retCodeReklYes:
                aAdvLink = modules['object'].getAdvPage()
                logging.info(u"Advertising...")
                for a in aAdvLink:
                    err = modules['object'].clickLinks(a)
                    logging.debug(u"Sleeping 10 sec.")
                    time.sleep(22)
                    if err[0]:
                        logging.error(err)
                        break

        if err == nbCommon.retCodeNetworkError:
            vTimeSleep = 1.30 * vTimeSleep if vTimeSleep < 800 else 900
        else:
            vTimeSleep = nbCommon.vTimeSleep

        err = modules['object'].errorCorrect(err)
        logging.debug(u"Sleeping %s sec." % vTimeSleep)
        time.sleep(vTimeSleep)
