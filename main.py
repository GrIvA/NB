#!/usr/bin/env python
#-*- coding: utf-8 -*-
import os, sys
import inspect
import time
import logging


plugin_dir = "plugins"

import plugins.base
import nbCommon

modules = {}


def loadPlugins(plugName):
    """Load plugins from plugin directory"""
    logging.debug(u"load module: ==> %s" % plugName)

    try:
        package_obj = __import__(plugin_dir + "." +  plugName)
        module_obj = getattr(package_obj, plugName)
        for elem in dir(module_obj):
            obj = getattr (module_obj, elem)
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

    logging.basicConfig(format = u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s', level = logging.DEBUG)
    err = loadPlugins(sys.argv[1])


    while (err[0] == 0) or (err == nbCommon.retCodeNetworkError):
        req = modules['object'].getPage()

        if req[0] == 0:
            err = modules['object'].analysePage()
            if err == 0:
                logging.info(u"Заглушка: Можем смотреть рекламу.")
            else:
                err = modules['object'].errorCorrect(err)
        time.sleep(20)
        #exit()




