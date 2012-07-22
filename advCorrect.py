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

    for a in ADVHash:
    	if ADVHash[a][0] == '*':
    		print '%s(%s)' % (ADVHash[a][1], ADVHash[a][2])
    		ADVHash[a][0] = raw_input("accept advertising? (Y/N)").upper()
        else:
            print "INFO: %s, STATUS: %s" %(ADVHash[a][1], ADVHash[a][0])

    f = open(vADVHashPath, "wb")
    pickle.dump(ADVHash, f)
    f.close()

