#!/usr/bin/env python
#-*- coding: utf-8 -*-
from grab import Grab
from grab.error import GrabNetworkError
from grab.error import GrabConnectionError
import logging
import nbCommon

class baseplugin (object):
    gr_module = 0
    def __init__(self):
        import ConfigParser
        logging.debug(u" ==> init")
        self.gr_module = Grab()
        try: self.gr_module.setup(proxy = nbCommon.proxy, proxy_type = nbCommon.proxy_type)
        except: pass
        self.gr_module.setup(reuse_referer = True)

        config = ConfigParser.ConfigParser()
        config.read(nbCommon.iniFile)
        logDir = config.get('main', 'log_dir')
        if logDir != '': self.gr_module.setup(log_dir = logDir)

    def LoadConfig(self):
        pass


    def getPage(self):
        return nbCommon.retCodeOK
        
    def getAdvPage(self):
        return []

    def clickLinks(self, Link):
        return nbCommon.retCodeOK

    def getHTTP (self, link):
        """
        Get http page
        """
        try:
            self.gr_module.go(link)
        except GrabNetworkError as e:
            logging.error(u"Error socket: %s" % e)
            return nbCommon.retCodeNetworkError
        except GrabConnectionError as e:
            logging.error(u"Error connection: %s" % e)
            return nbCommon.retCodeNetworkError
        else:
            return nbCommon.retCodeOK

    def analysePage(self):
        return nbCommon.retCodeOK

    def errorCorrect(self, error):
        return nbCommon.retCodeOK