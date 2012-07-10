#!/usr/bin/env python
#-*- coding: utf-8 -*-

retCodeOK = (0, "OK")
retCodeNoLoadPlug = (1, "Plugin does not exist.")
retCodeNoLoadLP = (2, "ERROR load login page.")
retCodeNoLogin = (3, "No login to site.")
retCodeReklYes = (4, "New reklama.")
retCodeClickLinksError = (5, "ERROR link analiser...")
retCodeClickLinksError2 = (6, "ERROR link analiser. No request fist post...")
retCodeClickLinksError3 = (7, "ERROR link analiser. No request second post...")
retCodeClickLinksError4 = (8, "ERROR link analiser. Non standart first ansver...")
retCodeClickLinksError5 = (9, "ERROR link analiser. Non standart second ansver...")

retCodeNetworkError = (900, "Network ERROR")

# *********************************
vTimeSleep = 20
#proxy = '127.0.0.1:8888'
#proxy_type = 'http'
