#!/usr/bin/env python
#-*- coding: utf-8 -*-

import os
import base
import time, re
from grab.tools import rex
import logging
import nbCommon
import pickle
from hashlib import md5

class NEOBUX(base.baseplugin):
    advCount = 0
    aServerHash = {}
    aADVHash = {}
    vCash = 0

    def LoadConfig(self):
        import ConfigParser
        config = ConfigParser.ConfigParser()
        config.read(nbCommon.iniFile)
        self.neo_login = config.get('neo_surf', 'neo_login')
        self.neo_pass  = config.get('neo_surf', 'neo_pass')
        self.neo_pass2 = config.get('neo_surf', 'neo_pass2')
        self.httpLink = config.get('neo_surf', "httpLink")
        self.httpLink2 = config.get('neo_surf', "httpLink2")
        self.httpLogin = config.get('neo_surf', "httpLogin")
        self.httpAdv = config.get('neo_surf', "httpAdv")
        self.neoCookieFile = config.get('neo_surf', "neoCookieFile")
        self.vServerHashPath = config.get('neo_surf', "vServerHashPath")
        self.vADVHashPath = config.get('neo_surf', "vADVHashPath")

        if os.path.exists(self.vADVHashPath): 
            f = open(self.vADVHashPath, "rb")
            self.aADVHash = pickle.load(f)
            f.close()
 

    def __init__(self):
        base.baseplugin.__init__(self)
        self.LoadConfig()
        logging.debug(u"==> init")
        self.gr_module.setup(reuse_referer = True)
        if not os.path.exists(self.neoCookieFile): 
            f = open(self.neoCookieFile, "w")
            f.close()
        self.gr_module.setup(cookiefile = self.neoCookieFile)
        # self.gr_module.setup(log_dir = 'd:\Work\Python\Surf_bux\Login\log')
        if os.path.exists(self.vServerHashPath): 
            f = open(self.vServerHashPath, "rb")
            self.aServerHash = pickle.load(f)
            f.close()

    def getHashServer(self, Server, hash):
        # TODO: len(hash) == 64
        if Server in self.aServerHash: pass
        else: 
            self.aServerHash[Server] = hash
            f = open(self.vServerHashPath, "wb")
            pickle.dump(self.aServerHash, f)
            f.close()

        return self.aServerHash[Server]


    def getPage (self):
        """
        Получение http страницы, анализ ее на ошибки"
        """
        return self.getHTTP("http://"+self.httpLink2+self.httpLink+str(int(time.time())))

    def w(self, key):
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

    def clickLinks(self, aLink):
        if self.getHTTP(aLink[1]+self.w(aLink[0][1][1:-1]))[0]:
            logging.error(u"clickLinks: ERROR load login page.")
            return nbCommon.retCodeNetworkError
        try:
            hash = re.search(r"try{df\('(.*?)'\);}", self.gr_module.response.body).group(1)
        except Exception, e:
            return nbCommon.retCodeClickLinksError6
        
        if self.getHTTP(aLink[1][:-7]+'v1/?s='+self.w(aLink[0][1][1:-1])+'&y='+self.getHashServer(aLink[1], hash)+'&noCache='+str(int(time.time())))[0]:
            return nbCommon.retCodeClickLinksError2
        if self.gr_module.response.body != "o=['0'];D();": return nbCommon.retCodeClickLinksError4
        if aLink[0][11] == "0.001": vSleep = 5
        elif aLink[0][11] == "0.005": vSleep = 22
        elif aLink[0][11] == "0.010": vSleep = 33
        elif aLink[0][11] == "'0.010'": vSleep = 33
        elif aLink[0][11] == "0.015": vSleep = 65
        else:
            logging.info(u"## New price is %s ###" % aLink[0][11])
            vSleep = 33
        time.sleep(vSleep)
        if self.getHTTP(aLink[1][:-7]+'v2/?s='+self.w(aLink[0][1][1:-1])+'&y='+self.getHashServer(aLink[1], hash)+'&noCache='+str(int(time.time())))[0]:
            return nbCommon.retCodeClickLinksError3
        # TODO Проконтролировать второй ответ
        price = re.search(r"\[(.*?,){2}(.*?)\]", self.gr_module.response.body).group(2)
        if price == "0": logging.info(u"Bad result. Click not accepted.")
        self.vCash += float(price)
        logging.info(u"Your cash %.3f $" % self.vCash)
        return nbCommon.retCodeOK

    def getAdvPage(self):
        logging.debug(u"load adv page.")
        aLink = []
        if self.getHTTP(self.httpAdv)[0]:
            logging.error(u"getAdvPage: ERROR load login page.")
            return aLink
        server = re.search(r'href="(http://ad.+a=l&l=)', self.gr_module.response.body)   
        for ad in re.findall(r'dr_l\(\[.*?]\)',self.gr_module.response.body):
            price = re.findall(r'(\'.*?\'|\d{1,2}(?:\.\d{3})?)', ad)
            # price[9] - Active link
            # price[11] - Price Link
            if (price[9] != '0') and (len(price[11])>3): 
                vADVHash = md5(price[4]+price[5]).hexdigest()
                if vADVHash in self.aADVHash:
                    if self.aADVHash[vADVHash][0] == 'Y': aLink.append([price, server.group(1)])
                else: 
                    self.aADVHash[vADVHash] = ['*', unicode(price[4], "cp1252"), unicode(price[5], "cp1252")]
                    logging.info(u"Add new adv... %s" % unicode(price[4], "cp1252"))
                f = open(self.vADVHashPath, "wb")
                pickle.dump(self.aADVHash, f)
                f.close()
        return aLink

    def login2site(self):
        # Clear Cookie
        f = open(self.neoCookieFile, "w")
        f.close()

        logging.debug(u"Wait 5 sec. and trying to login...")
        time.sleep(5)
        login_fields = {}
        if self.getHTTP(self.httpLogin)[0]:
            logging.error(u"NEO: ERROR load login page.")
            return nbCommon.retCodeNoLoadLP

        login_fields['lg'] = self.w(rex.rex_text(self.gr_module.response.body, re.compile("lg1\('(\w*.)'")))
        login_fields['img'] = self.gr_module.xpath('//iframe[@class="mbxm"]').get('src')

        login_fields['Kf1'] = self.gr_module.xpath('//input[@id="Kf1"]').get('name')
        login_fields['Kf2'] = self.gr_module.xpath('//input[@id="Kf2"]').get('name')
        login_fields['Kf3'] = self.gr_module.xpath('//input[@id="Kf3"]').get('name')
        login_fields['Kf4'] = self.gr_module.xpath('//input[@id="Kf4"]').get('name')
        login_fields['lge'] = self.gr_module.xpath('//input[@name="lge"]').get('value')
        login_fields['login'] = self.gr_module.xpath('//input[@name="login"]').get('value')

        self.getHTTP(login_fields['img'])
        img_url = self.gr_module.xpath('//div[@id="a"]/img').get('src')
        vCaptcha = raw_input("https://img.neobux.com"+img_url+"  ==> Input 5 symvols: ")
        login_fields['captcha'] = vCaptcha.upper()
        # print login_fields

        logging.debug(u"login ==> POST data")
        self.gr_module.setup(post='lge='+login_fields['lge']+'&'+
                                   login_fields['Kf1']+login_fields['lg'][2]+'='+self.neo_login+'&'+
                                   login_fields['Kf2']+login_fields['lg'][6]+'='+self.neo_pass+'&'+
                                   login_fields['Kf4']+login_fields['lg'][14]+'='+self.neo_pass2+'&'+
                                   login_fields['Kf3']+login_fields['lg'][10]+'='+login_fields['captcha']+'&'+
                                   'login='+login_fields['login'])
        return self.getHTTP(self.httpLogin)


    def analysePage(self, err):
        if err[0]: return err

        if self.gr_module.response.code != 200:
            logging.error(u"ERROR: %d" % self.gr_module.response.code)
            return nbCommon.retCodeNetworkError

        #Может нужно залогинится?
        if self.gr_module.response.body[1] == '0' or  len(self.gr_module.response.body) > 300:
            logging.error(u"NEO: login ERROR.")
            return nbCommon.retCodeNoLogin
        aStatus = self.gr_module.response.body[1:].split(",")
        logging.info(u"cash: %s.%s$, adv: %s" % (aStatus[7][:-1], aStatus[8][1:], aStatus[18]))
        self.httpLink2 = aStatus[29][1:-2]
        if (aStatus[18] != '0') :
            self.advCount = aStatus[3]
            return nbCommon.retCodeReklYes
        return nbCommon.retCodeOK

    def errorCorrect(self, err):
        if err[0] == 0: return nbCommon.retCodeOK
        elif err == nbCommon.retCodeNoLogin:  # Login
            return self.login2site()
        elif err == nbCommon.retCodeNetworkError: # Network Connection
            return nbCommon.retCodeOK
        return base.baseplugin.errorCorrect(self, err) # Other Error