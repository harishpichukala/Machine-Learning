# -*- coding: utf-8 -*-
"""
Created on Sun Dec 20 18:02:14 2015

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

def LoadData(path1, path2, model):
    
    quantizer = Quantization(model.getNumCutOffs())
    quantizer.setCutOffs(model.getCutOffs())
        
    faceData = ReadDataSet(path1)    
    quantizedFaceData = quantizer.runQuantization(faceData)
    del faceData    

    nonfaceData = ReadDataSet(path2)
    quantizedNonFaceData = quantizer.runQuantization(nonfaceData)

    del nonfaceData
    return quantizedFaceData, quantizedNonFaceData
    
############### main function #################    
if __name__ == '__main__':  
    SetupPath()
    from ReadDataSet import *
    from Quantization import *
    from SemiNaive import *
    from Model import *
    
    
    model = Model(GetCurrentPath() + '/Models/ProbabilityTables.pkl')    
    model.read()        

    [faces, nonfaces] = LoadData(GetCurrentPath() + '/Data/CalTech/test/faces/', \
                                 GetCurrentPath() + '/Data/CalTech/test/non-faces/', \
                                 model)
                                  
    
#    faces = [[1,1,0,1],[1,0,1,1],[1,1,1,1]]
#    nonfaces = [[1,1,1,0],[0,1,0,1],[0,1,1,0]]
#    faces = np.array(faces).T
#    nonfaces = np.array(nonfaces).T 
    
    classifier = SemiNaive(faces.shape[0], model.getNumCutOffs(), model.getSubgroupSize())   
    classifier.loadModel(model)
    likelihoodClass1 = classifier.test(faces)
    print '------------------------------------'
    likelihoodClass2 = classifier.test(nonfaces)
    
    TP = TP1 = TP2 = 0
    FP = 0
    Threshold = 0
    with open("Output.txt", "w") as output_file:
        for i in range(0,likelihoodClass1.shape[0]):
            output_file.write("%d %f\n" % (1, likelihoodClass1[i]))
            if (likelihoodClass1[i] >= Threshold): TP1 += 1
            else: FP += 1
           
        for i in range(0,likelihoodClass2.shape[0]):
            output_file.write("%d %f\n" % (0, likelihoodClass2[i]))    
            if (likelihoodClass2[i] < Threshold): TP2 += 1
            else: FP += 1            
            
        TP = TP1 + TP2    
        print('Acc = %f (%f %f)' % (100 * TP/float(TP+FP), \
                                  100 * TP1/float(likelihoodClass1.shape[0]), \
                                  100 * TP2/float(likelihoodClass2.shape[0])))            
           
    del faces
    del nonfaces           