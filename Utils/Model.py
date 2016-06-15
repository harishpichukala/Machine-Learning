# -*- coding: utf-8 -*-
"""
Created on Sun Dec 20 11:23:43 2015

@author: ymlui
"""

from pylab import *
import numpy as np
import pickle


class Model:
    def __init__(self, filename):
        self.filename = filename
        
    def setCutOffs(self, cutoffs):
        self.numCoeffs = cutoffs.shape[0]
        self.cutoffs = cutoffs    
                
    def getCutOffs(self): 
        return self.cutoffs
        
    def getNumCutOffs(self):
        return self.numCutOffs
        
    def setDataSize(self, dataSize):
        self.dataSize = dataSize

    def getDataSize(self):
        return self.dataSize
        
    def setSubgroupSize(self, subgroupSize):
        self.subgroupSize = subgroupSize
       
    def getSubgroupSize(self):
        return self.subgroupSize
        
    def setNumClass1(self, num):
        self.numClass1 = num

    def getNumClass1(self):
        return self.numClass1
        
    def setNumClass2(self, num):
        self.numClass2 = num
    
    def getNumClass2(self):
        return self.numClass2
        
    def setSubgroups(self, subgroups):
        self.subgroups = subgroups    
        
    def getSubgroups(self):
        return self.subgroups
        
    def setTableClass1(self, tableClass1):
        self.tableClass1 = tableClass1
    
    def getTableClass1(self):
        return self.tableClass1
        
    def setTableClass2(self, tableClass2):
        self.tableClass2 = tableClass2    
        
    def getTableClass2(self):
        return self.tableClass2
        
    def setGoodness(self, goodness):
        self.goodness = goodness
        
    def getGoodness(self):
        return self.goodness
        
        
    def write(self):
        with open(self.filename, 'wb') as output:
            pickle.dump(self, output, pickle.HIGHEST_PROTOCOL)
        
        
    def read(self):
        with open(self.filename, 'rb') as input:
            obj = pickle.load(input)
            
        self.subgroupSize = obj.subgroupSize
        self.dataSize = obj.dataSize
        self.numCoeffs = obj.numCoeffs
        self.numClass1 = obj.numClass1
        self.numClass2 = obj.numClass2
        self.cutoffs = obj.cutoffs    
        self.numCutOffs = len(self.cutoffs)

        self.subgroups = obj.subgroups
        self.tableClass1 = obj.tableClass1
        self.tableClass2 = obj.tableClass2   
        self.goodness = obj.goodness
        