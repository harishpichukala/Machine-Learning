# -*- coding: utf-8 -*-
"""
Created on Sat Dec 12 15:32:27 2015

@author: ymlui
"""

import numpy as np
from pylab import *
import matplotlib.pyplot as plt

HISTOGRAM_SIZE = 256

class Quantization:
    def __init__(self, num):
        self.cutoffs = np.zeros(num, dtype=np.int)
        self.num = num
        
    def getHistogram(self, imdataRecord, bDisplay=False):
        alldata = []
        for i in range(0, size(imdataRecord)):
            data = array(imdataRecord[i].getDataBuffer()).flatten()
            alldata.append(data)
        
        alldata = array(alldata).flatten()   
    
        [hist, bin_edges] = np.histogram(alldata, bins = range(HISTOGRAM_SIZE))
    
        if (bDisplay):
            plt.bar(bin_edges[:-1], hist, width = 1)
            plt.show()  
            print sum(hist)
            
        return hist, sum(hist)

    def initQuantization(self, imdataRecord):
        #compute histogram
        [hist, total] = self.getHistogram(imdataRecord)
    
        for i in range(0,self.num-1):
            if (i>0):
                self.cutoffs[i] = self.cutoffs[i-1] + 1

            bucket = 0
            for j in range(self.cutoffs[i],HISTOGRAM_SIZE):
                bucket += hist[j]
                if (bucket > total/self.num): break
                
                self.cutoffs[i] = j    
                if (bucket == total/self.num): break
            
        self.cutoffs[self.num-1] = HISTOGRAM_SIZE-1        
        print self.cutoffs    
        
        return self.cutoffs

    def setCutOffs(self, cutoffs):
        self.cutoffs = cutoffs        
        
    def runQuantization(self, imdataRecord):
        m = size(imdataRecord)
        n = (array(imdataRecord[0].getDataBuffer()).flatten()).shape[0]
    
        quantizedData = np.zeros((n,m), dtype=np.int)
        for i in range(0, size(imdataRecord)):
            data = array(imdataRecord[i].getDataBuffer()).flatten()
            data = data.astype(int)
            
            idn = 0
            idx = [ii for ii,jj in enumerate(data) if jj <= self.cutoffs[0] ]   
            data[idx] = idn
            idn += 1
            
            for j in range(1, self.num):
                idx = [ii for ii,jj in enumerate(data) if jj >  self.cutoffs[j-1] and 
                                                          jj <= self.cutoffs[j] ]  
                data[idx] = idn
                idn += 1
            
            
#            x = data.reshape(imdataRecord[i].getImgWidth(), imdataRecord[i].getImgHeight())
#            print x
#            imshow(x, cmap='Greys_r')
#            show()
            
            quantizedData[:,i] = data
            
        return quantizedData
            
            
            