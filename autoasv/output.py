"""
Output information
"""

#Import modules
import os
from os import path
import sys
import numpy as np
from sys import exit

def outputfiles(samplelist,runlist,forwardlist,reverselist,projectdir):
    outputfilelist=[]
    for (sample,run,forward) in zip(samplelist,runlist,forwardlist):
        forwardfile=projectdir+'/1-Primersclipped/'+run+'/'+sample+'_1.fq.gz'
        outputfilelist.append(forwardfile)
        forwardfile_rev=projectdir+'/1-Primersclipped_rev/'+run+'/'+sample+'_1.fq.gz'
        outputfilelist.append(forwardfile_rev)
    return(outputfilelist)
