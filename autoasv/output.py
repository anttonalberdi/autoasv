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
    #for (sample,run,reverse) in zip(samplelist,runlist,reverselist):
    #    reversefile=projectdir+'/1-Primersclipped/'+run+'/'+sample+'_2.tmp.fq.gz'
    #    outputfilelist.append(reversefile)
    #    reversefile_rev=projectdir+'/1-Primersclipped/'+run+'/'+sample+'_2rev.tmp.fq.gz'
    #    outputfilelist.append(reversefile_rev)
    return(outputfilelist)
