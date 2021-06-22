"""
Read input information
"""

#Import modules
import os
import sys
from sys import exit

def dir_path(string):
    if os.path.isdir(string):
        return string
    else:
        raise NotADirectoryError(string)

def inputdata(input):
    print(input)
