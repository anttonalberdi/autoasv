#!/usr/bin/env python

import autoasv
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

#Get arguments

parser = argparse.ArgumentParser(description='Runs BAMSE pipeline.')
parser.add_argument('-i', help="Data information file", dest="input", required=True)
parser.add_argument('-d', help="Working directory of the project", dest="workdir", required=True)
parser.add_argument('-f', help="Forward primer sequence", dest="primer_for", required=True)
parser.add_argument('-r', help="Reverse primer sequence", dest="primer_rev", required=True)
parser.add_argument('-a', help="Expected average amplicon length", dest="ampliconlength", required=True)
parser.add_argument('-x', help="Absolute path to the taxonomy database", dest="taxdb", required=True)
args = parser.parse_args()

# Translate arguments
input=args.input
workdir=args.workdir
primer_for=args.primer_for
primer_rev=args.primer_rev
ampliconlength=args.ampliconlength
taxdb=args.taxdb

def main():
    print(input)
    print(workdir)
    print(primer_for)
    print(primer_rev)
    print(ampliconlength)
    print(taxdb)
