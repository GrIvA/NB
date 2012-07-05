#!/usr/bin/env python
#-*- coding: utf-8 -*-

import base
import time, re
from grab.tools import rex

class NEOBUX(base.baseplugin):
    neo_login = 'griva99'
    neo_pass  = '%40OaoIkgoIwwy_71'
    neo_pass2 = ''
    httpLink = "http://ad.neobux.com/adalert/g/?t="
    httpLogin = "https://www.neobux.com/m/l/"
#    httpLink = "http://spystorm.net/test_function.html?t="
#    httpLogin = "http://spystorm.net/test_noformat.html"

    def __init__(self):
        base.baseplugin.__init__(self)
        print "NEO: ==> init"

    def getPage (self):
        """
        Получение http страницы, анализ ее на ошибки"
        """
        return self.getHTTP(self.httpLink+str(int(time.time())))

    def login2site(self):
        def w(key):
            k='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/='
            j = 0; r = ''
            while j < len(key):
                e1 = k.find(key[j])
                e2 = k.find(key[j+1])
                e3 = k.find(key[j+2])
                e4 = k.find(key[j+3])
                j += 4
                c1 = (e1<<2)|(e2>>4)
                c2 = ((e2&15)<<4)|(e3>>2)
                c3 = ((e3&3)<<6)|e4
                r = r + chr(c1)
                if e3 != 64: r = r + chr(c2)
                if e4 != 64: r = r + chr(c3)
            return r

        print " NEO: ==> Ждем 5 сек. и логинимся..."
        time.sleep(5)
        login_fields = {}
        if self.getHTTP(self.httpLogin)[0]:
            print "NEO: ERROR load login page."
            return 2

        login_fields['lg'] = w(rex.rex_text(self.gr_module.response.body, re.compile("lg1\('(\w*.)'")))
        login_fields['img'] = self.gr_module.xpath('//iframe[@class="mbxm"]').get('src')

        login_fields['Kf1'] = self.gr_module.xpath('//input[@id="Kf1"]').get('name')
        login_fields['Kf2'] = self.gr_module.xpath('//input[@id="Kf2"]').get('name')
        login_fields['Kf3'] = self.gr_module.xpath('//input[@id="Kf3"]').get('name')
        login_fields['Kf4'] = self.gr_module.xpath('//input[@id="Kf4"]').get('name')
        login_fields['lge'] = self.gr_module.xpath('//input[@name="lge"]').get('value')
        login_fields['login'] = self.gr_module.xpath('//input[@name="login"]').get('value')

        #g_img = self.gr_module.clone()
        self.getHTTP(login_fields['img'])
        img_url = self.gr_module.xpath('//div[@id="a"]/img').get('src')
        #self.gr_module.adopt(g_img)
        login_fields['captcha'] = raw_input("https://img.neobux.com"+img_url+"  ==> Input 5 symvols: ")
        print login_fields

        print "NEO:login ==> Формируем данные POST запроса"
        #self.gr_module.setup(reuse_referer = False)
        #self.gr_module.setup(referer=self.httpLogin)
        self.gr_module.setup(post='lge='+login_fields['lge']+'&'+
                                   login_fields['Kf1']+login_fields['lg'][2]+'='+self.neo_login+'&'+
                                   login_fields['Kf2']+login_fields['lg'][6]+'='+self.neo_pass+'&'+
                                   login_fields['Kf4']+login_fields['lg'][14]+'='+self.neo_pass2+'&'+
                                   login_fields['Kf3']+login_fields['lg'][10]+'='+login_fields['captcha']+'&'+
                                   'login='+login_fields['login'])

        self.getHTTP(self.httpLogin)
        #self.gr_module.setup(reuse_referer = True)
        #print self.gr_module.response.body
        return 0


    def analysePage(self):
        """
        ERROR:
            1 - login
        """
        if self.gr_module.response.code != 200:
            print "ERROR: %d" % self.gr_module.response.code
            return 900

        print self.gr_module.response.body
        #Может нужно залогинится?
        if self.gr_module.response.body[1] == '0' or  len(self.gr_module.response.body) > 300:
            print "NEO: login ERROR."
            return 1
        return 0

    def errorCorrect(self, error):
        if error == 1:  # Login
            return self.login2site()
        return 0