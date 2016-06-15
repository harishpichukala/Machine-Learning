# -*- coding: utf-8 -*-
"""
Created on Fri Dec 11 10:26:02 2015

@author: ymlui
"""
import numpy as np
from Img import *
from scipy import ndimage

def ExtractEdge(imdata):
    dx = ndimage.sobel(imdata.getDataBuffer(), 0)
    dy = ndimage.sobel(imdata.getDataBuffer(), 1)
    mag = np.hypot(dx, dy)
    mag = mag.astype('int32')
    mag = 255 * mag / np.max(np.max(mag))
    
    imdata.setDataBuffer(mag)
    
    return imdata

    
    
def Preprocessing(img, option='edge'):
    imdata = Img(img)
    
    if (option=='raw' or option=='RAW' or option=='Raw'):
        imdata.setGrayscaleBuffer()
        imdata.znorm()
        imdata.normalize()
    elif (option=='edge' or option=='EDGE' or option=='Edge'):    
        imdata.setGrayscaleBuffer()
        imdata.znorm()
        imdata = ExtractEdge(imdata)
        
    #imdata.display()    
    return imdata    