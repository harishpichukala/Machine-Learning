# -*- coding: utf-8 -*-
"""
Created on Fri Dec 11 08:02:52 2015

@author: ymlui
"""

import os
from PIL import Image
from pylab import *
from Preprocessing import *


def ReadDataSet(datapath):
    dirfiles = os.listdir(datapath)    

    data = []
    #for i in range(0,len(dirfiles)):
    for i in range(0,min(2000,len(dirfiles))):
    
        fname = dirfiles[i]
        if (fname[0] != '.'):
            img = Image.open(datapath + fname)
        
            data.append(Preprocessing(img, 'raw'))
            img.close()
        
            print i

    return data     