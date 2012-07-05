#!/usr/bin/env python
#-*- coding: utf-8 -*-
import os, sys
import inspect
import time
import logging


plugin_dir = "plugins"

import plugins.base

modules = {}


def loadPlugins(plugName):
    """Load plugins from plugin directory"""
    logging.debug(u"load module: ==> %s" % plugName)
    package_obj = __import__(plugin_dir + "." +  plugName)
    module_obj = getattr(package_obj, plugName)
    for elem in dir(module_obj):
        obj = getattr (module_obj, elem)
        # Это класс? Класс производный от baseplugin?
        if inspect.isclass(obj) and issubclass(obj, plugins.base.baseplugin):
            # Создаем экземпляр и выполняем функцию run
            modules['object'] = obj()
            return 0
        else: return 1

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print """ USE: python main.py plugNAME
    Where 'plugNAME' - name your plugin from plugins dir.
        """
        exit()

    logging.basicConfig(format = u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s', level = logging.DEBUG)
    if loadPlugins(sys.argv[1]): logging.critical(u"ERROR: Can't load module...")

    err = 0
    while err == 0:
        req = modules['object'].getPage()

        if req[0] != 0:
            logging.error(u"main: ERROR %s (%s)" % (req[0], req[1]))
        else:
            err = modules['object'].analysePage()
            if err == 0:
                logging.info(u"Заглушка: Можем смотреть рекламу.")
            else:
                err = modules['object'].errorCorrect(err)
        time.sleep(20)
        #exit()



