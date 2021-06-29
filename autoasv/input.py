"""
Input information
"""

#Import modules
import os
from os import path
import sys
import numpy as np
from sys import exit

def dir_path(string):
    if os.path.isdir(string):
        return string
    else:
        raise NotADirectoryError(string)

def inputdata(input):
    inputtable=np.loadtxt(open(input, "rb"), dtype='str', delimiter=",")
    return(inputtable)

def testrawfiles(forwardlist,reverselist):
    #List of existance of forward reads
    forwardexist=[]
    for f in forwardlist:
        if path.exists(f):
            forwardexist.append(True)
        else:
            forwardexist.append(False)

    #List of existance of reverse reads
    reverseexist=[]
    for f in reverselist:
        if path.exists(f):
            reverseexist.append(True)
        else:
            reverseexist.append(False)

    #Print error
    if not all(forwardexist) or not all(reverseexist):
        print("\nERROR!")
        print("There are errors in the input file.")

    #Print incorrect files
    for f in forwardlist:
        if not path.exists(f):
            print("\tRaw file "+str(f)+" does not exist.")
    for r in reverselist:
        if not path.exists(r):
            print("\tRaw file "+str(r)+" does not exist.")

    #Stop pipeline if there are errors
    if not all(forwardexist) or not all(reverseexist):
        sys.exit(0)

def softlinks(samplelist,runlist,forwardlist,reverselist,projectdir):
    if not os.path.isdir(os.path.join(os.path.abspath(projectdir),"0-Rawdata")):
        os.mkdir(os.path.join(os.path.abspath(projectdir),"0-Rawdata"))

    for run in set(runlist):
        if not os.path.isdir(os.path.join(os.path.abspath(projectdir),"0-Rawdata",run)):
            os.mkdir(os.path.join(os.path.abspath(projectdir),"0-Rawdata",run))

    for (sample,run,forward) in zip(samplelist,runlist,forwardlist):
        samplename=sample+'_1.fq.gz'
        if not os.path.isfile(os.path.join(os.path.abspath(projectdir),"0-Rawdata",run,samplename)):
            os.symlink(forward, os.path.join(os.path.abspath(projectdir),"0-Rawdata",run,samplename))
    for (sample,run,reverse) in zip(samplelist,runlist,reverselist):
        samplename=sample+'_2.fq.gz'
        if not os.path.isfile(os.path.join(os.path.abspath(projectdir),"0-Rawdata",run,samplename)):
            os.symlink(reverse, os.path.join(os.path.abspath(projectdir),"0-Rawdata",run,samplename))

#Create and append information to the parameters file
def createconfig(input,autoasvpath,projectdir,paramsfile,threads,logfile,primer_for,primer_rev):
    f = open(str(paramsfile), "a")
    f.write("#autoASV core paths\n")
    f.write("autoasvpath:\n "+str(autoasvpath)+"\n")
    f.write("projectdir:\n "+str(projectdir)+"\n")
    f.write("inputfile:\n "+str(input)+"\n")
    f.write("paramsfile:\n "+str(paramsfile)+"\n")
    f.write("logfile:\n "+str(logfile)+"\n")
    f.write("threads:\n "+str(threads)+"\n")
    f.write("primer_for:\n "+str(primer_for)+"\n")
    f.write("primer_rev:\n "+str(primer_rev)+"\n")
