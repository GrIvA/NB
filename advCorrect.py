#!/usr/bin/env python
#-*- coding: utf-8 -*-

import os
import pickle

vADVHashPath = 'Trash/ADVHash'

if __name__ == '__main__':
    if os.path.exists(vADVHashPath): 
        f = open(vADVHashPath, "rb")
        ADVHash = pickle.load(f)
        f.close()
        print 'Load ADV array...'
    else:
    	print "Nothing ADV array... sorry"
    	exit()
    SaveFlag = False
    for a in ADVHash:
    	if ADVHash[a][0] == '*':
            SaveFlag = True
            print '%s(%s)' % (ADVHash[a][1], ADVHash[a][2])
    
    if SaveFlag: key = raw_input("accept advertising? (Y/N)").upper()
    else: 
        print "      ... Nothing."
        exit()
    SaveFlag = False
    if key == "Y":
        for a in ADVHash:
            if ADVHash[a][0] == "*":
                SaveFlag = True
                ADVHash[a][0] = "Y"
    if SaveFlag:
        f = open(vADVHashPath, "wb")
        pickle.dump(ADVHash, f)
        f.close()
        os.remove("nothing.load")

