#!/usr/bin/env python

import os
from sys import exit
from glob import glob
import argparse
import subprocess
import ruamel.yaml
import pathlib
import re
import time
from shutil import which
from Bio import SeqIO
import numpy as np
import statistics

import autoasv
from readinput import dir_path
from log import initiallog,settingslog

#######
# Get and process arguments
#######

parser = argparse.ArgumentParser(description='Runs autoASV pipeline.')

#Mandatory arguments
parser.add_argument('-i','--input', help="Data information file", dest="input", type=str, required=True)
parser.add_argument('-d','--dir', help="Working directory of the project", dest="projectdir", type=dir_path, required=True)
parser.add_argument('-f','--forward', help="Forward primer sequence", dest="primer_for", type = str, required=True)
parser.add_argument('-r','--reverse', help="Reverse primer sequence", dest="primer_rev", type = str, required=True)
parser.add_argument('-a','--ampliconlength', help="Expected average amplicon length", type = int, dest="ampliconlength", required=True)
parser.add_argument('-x','--taxonomydb', help="Absolute path to the taxonomy database", dest="taxdb", type=str, required=True)

#Optional non-parameter arguments
parser.add_argument('-t','--threads', help="Number of threads", dest="threads", type=int, required=False)
parser.add_argument('-p','--paramsfile', help="Absolute path to the parameters file that BAMSE will create", dest="paramsfile", required=False)
parser.add_argument('-l','--logfile', help="Absolute path to the log file that BAMSE will create", dest="logfile", required=False)
parser.add_argument('-w','--overwrite', help="Overwrite contents in the working directory of the project", action='store_true', dest="overwrite", required=False)

#Optional parameter arguments
parser.add_argument('-n','--minampliconlength', help="Expected minimum amplicon length", dest="minampliconlength", type=int, required=False)
parser.add_argument('-m','--maxampliconlength', help="Expected maximum amplicon length", dest="maxampliconlength", type=int, required=False)
parser.add_argument('--maxerrors', help="Maximum number of expected errors per read", dest="maxerrors", type=int, required=False)
parser.add_argument('--minoverlap', help="Minimum overlap between reads for merging", dest="minoverlap", type=int, required=False)
parser.add_argument('--trimforward', help="Trimming length of forward reads", dest="trim_for", type=int, required=False)
parser.add_argument('--trimreverse', help="Trimming length of reverse reads", dest="trim_rev", type=int, required=False)
parser.add_argument('--adaptorforward', help="Forward adaptor sequence", dest="adaptor_for", type = str, required=False)
parser.add_argument('--adaptorreverse', help="Reverse adaptor sequence", dest="adaptor_rev", type = str, required=False)
parser.add_argument('--maxreads', help="Maximum number of reads to be analysed to find optimal trimming parameters", dest="maxreads", type=int, required=False)
parser.add_argument('--taxfilter', help="Taxonomy filtering threshold", dest="taxfilter", choices=['kingdom', 'phylum', 'class','order','family','genus','species'], required=False)
parser.add_argument('--chimerafold', help="Minimum fold to consider parent ASVs for chimera detection", dest="chimerafold", type=int, required=False)
parser.add_argument('--copythreshold', help="Relative copy number threshold to consider an ASV in a sample", dest="copythreshold", type=float, required=False)

args = parser.parse_args()

### Translate arguments

#Mandatory arguments
input=args.input
projectdir=args.projectdir
primer_for=args.primer_for
primer_rev=args.primer_rev
ampliconlength=args.ampliconlength
taxdb=args.taxdb

#Optional non-parameter arguments
threads=args.threads
paramsfile=args.paramsfile
logfile=args.logfile
overwrite=args.overwrite

#Optional parameter arguments
minampliconlength=args.minampliconlength
maxampliconlength=args.maxampliconlength
maxerrors=args.maxerrors
minoverlap=args.minoverlap
trim_for=args.trim_for
trim_rev=args.trim_rev
adaptor_for=args.adaptor_for
adaptor_rev=args.adaptor_rev
maxreads=args.maxreads
taxfilter=args.taxfilter
chimerafold=args.chimerafold
copythreshold=args.copythreshold

#######
# Declare default values
#######

if primer_for is None:
    primF='noprimer_for'

if primer_rev is None:
    primF='noprimer_rev'

if threads is None:
    threads=1

if paramsfile is None:
    paramsfile=os.path.join(os.path.abspath(projectdir),"autoasv.yaml")

if logfile is None:
    logfile=os.path.join(os.path.abspath(projectdir),"autoasv.log")

if minampliconlength is None:
    minampliconlength=int(ampliconlength)-15

if maxampliconlength is None:
    maxampliconlength=int(ampliconlength)+15

if maxerrors is None:
    maxerrors=2

if minoverlap is None:
    minoverlap=20

if trim_for is None:
    trim_for='auto'

if trim_rev is None:
    trim_rev='auto'

if adaptor_for is None:
    adaptor_for='AGATCGGAAGAGCACACGTCTGAACTCCAGTCA'

if adaptor_rev is None:
    adaptor_rev='AGATCGGAAGAGCGTCGTGTAGGGAAAGAGTGT'

if maxreads is None:
    maxreads='auto'

if taxfilter is None:
    taxfilter='kingdom'

if chimerafold is None:
    chimerafold='2'

if copythreshold is None:
    copythreshold='0.0001'

#######
# Log
#######

#Pipeline presentation log
initiallog()

#Settings log
settingslog(input,projectdir,paramsfile,logfile,taxdb,primer_for,primer_rev,ampliconlength,minampliconlength,maxampliconlength,maxerrors,minoverlap,trim_for,trim_rev,maxreads,chimerafold,copythreshold,taxfilter,adaptor_for,adaptor_rev)

#######
# Read input file
#######

inputdata()

#def main():
#    print(input)
