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
args = parser.parse_args()

# Translate arguments
input=args.input
workdir=args.workdir


def main():
    print(input)
    print(workdir)
