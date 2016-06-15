# -*- coding: utf-8 -*-
"""
Created on Fri Dec 11 07:55:27 2015

@author: ymlui
"""

import sys, os
import numpy as np


def GetCurrentPath():
    return os.path.dirname(os.path.realpath(__file__))

def SetupPath():
    newpath = GetCurrentPath() + '/Utils'
    sys.path.append(newpath)

    newpath = GetCurrentPath() + '/Algo'
    sys.path.append(newpath)

def LoadData(path1, path2):
    faceData = ReadDataSet(path1)
    
    quantizer = Quantization(settings.NUM_CUTOFF)
    cutoffs = quantizer.initQuantization(faceData)
        
    quantizedFaceData = quantizer.runQuantization(faceData)
    del faceData    

    nonfaceData = ReadDataSet(path2)
    quantizedNonFaceData = quantizer.runQuantization(nonfaceData)

    del nonfaceData
    return quantizedFaceData, quantizedNonFaceData, cutoffs
    
############### main function #################    
if __name__ == '__main__':  
    SetupPath()
    from ReadDataSet import *
    from Quantization import *
    from SemiNaive import *
    from Model import *
    import settings 
    
    settings.init()
    
    [faces, nonfaces, cutoffs] = LoadData(GetCurrentPath() + '/Data/CalTech/train/faces/', \
                                 GetCurrentPath() + '/Data/CalTech/train/non-faces/')
    
    model = Model(GetCurrentPath() + '/Models/ProbabilityTables.pkl')    
    model.setCutOffs(cutoffs)         
         
    
#    faces = [[1,1,0,1],[1,0,1,1]]
#    nonfaces = [[1,1,1,0],[0,1,0,1]]
#    faces = np.array(faces).T
#    nonfaces = np.array(nonfaces).T      
    
    classifier = SemiNaive(faces.shape[0], settings.NUM_CUTOFF, settings.SUBGROUP_SIZE)    
    classifier.train(faces, nonfaces, model)
    
    del faces
    del nonfaces