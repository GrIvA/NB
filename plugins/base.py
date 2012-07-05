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
        logging.debug(u" ==> init")
        self.gr_module = Grab()
        self.gr_module.setup(proxy = '127.0.0.1:8888', proxy_type = 'http')
        self.gr_module.setup(reuse_referer = True)
    
    def getPage(self):
        pass

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
        """
        Общий анализ страницы.
        Важно убедиться, что это не страница ощибки,
        регистрации или еще какое-то сообщение.

        Если все нормально, возвращает 0, иначе, код ощибки, который обязан
        знать обработчик ошибок класса.

        """
        return nbCommon.retCodeOK

    def errorCorrect(self, error):
        return nbCommon.retCodeOK