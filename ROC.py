# -*- coding: utf-8 -*-
"""
Created on Tue Nov  3 11:00:31 2015

@author: ymlui
"""
import sys, getopt, os

def GetCurrentPath():
    return os.path.dirname(os.path.realpath(__file__))

def SetupPath():
    newpath = GetCurrentPath() + '/Utils'
    sys.path.append(newpath)
    
    
############### main function #################
if __name__ == '__main__':
    SetupPath()
    from ComputeROC import *
    
    roc = ComputeSimilarityROC('Output.txt')
    roc.MakeROC()