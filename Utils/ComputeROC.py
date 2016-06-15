# -*- coding: utf-8 -*-
"""
Created on Tue Nov  3 10:56:08 2015

@author: ymlui
"""

import csv
from pylab import *
import matplotlib.pyplot as plt

class ComputeROC:
    def __init__(self, infile):
        [self.labels, self.scores] = self.ReadFile(infile)
    

    def ReadFile(self, infile):
        label = []
        dist = []
        with open(infile, 'r') as csvfile:
            reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
            for row in reader:
                label.append(int(row[0]))
                dist.append(float(row[1]))
            
        return array(label), array(dist)        


    # pure virtual function    
    def SortData(): pass
        
    def MakeROC(self):
        # calling a virtual function - Template design pattern
        [sortedScores, idx] = self.SortData()
    
        P = sum(self.labels)
        N = len(self.scores) - P
    
        R_TP = []
        R_FP = []
        TP = 0
        FP = 0
        prev = float('Inf')
        for i in range(0,len(self.labels),1):
            if (sortedScores[i] != prev):
                R_TP.append(float(TP) / float(P))
                R_FP.append(float(FP) / float(N))
            
                prev = sortedScores[i]

            if (array(self.labels[idx[i]]) == 1): 
                TP = TP + 1
            else:
                FP = FP + 1
            
                 
        #plt.semilogx(R_FP, R_TP, linewidth=2.0)         
        plt.plot(R_FP, R_TP, linewidth=2.0) 
        plt.xlabel('False Positive')
        plt.ylabel('True Positive')
        plt.show()         


class ComputeDistROC(ComputeROC): 
    def __init__(self, infile):
        ComputeROC.__init__(self, infile)
        
        
    def SortData(self):
        # sort score in ascending order for distance
        data = sorted((e,i) for i,e in enumerate(self.scores))
        
        sortedScores = [i[0] for i in data]
        idx = [i[1] for i in data]
        
        return sortedScores, idx
        
        
class ComputeSimilarityROC(ComputeROC): 
    def __init__(self, infile):
        ComputeROC.__init__(self, infile)
        
        
    def SortData(self):
        # sort score in descending order for similarity
        data = sorted(((e,i) for i,e in enumerate(self.scores)), reverse=True)
        
        sortedScores = [i[0] for i in data]
        idx = [i[1] for i in data]
        
        return sortedScores, idx        
