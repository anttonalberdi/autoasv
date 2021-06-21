"""
Build autoASV
"""

import sys
import os.path
from setuptools import setup, Extension, find_packages

import pathlib
# The directory containing this file
HERE = pathlib.Path(__file__).parent

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="autoasv",
    version="1.0",
    author="Antton Alberdi",
    author_email="anttonalberdi@gmail.com",
    description="Automatic amplicon sequencing data processing pipeline",
    long_description=long_description,
    long_description_content_type="text/markdown",
    scripts=['bin/autoasv'],
    url="https://github.com/anttonalberdi/autoasv",
    project_urls={
        "Bug Tracker": "https://github.com/anttonalberdi/autoasv/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'setuptools',
        'pandas >= 0.22.0',
        'numpy >= 1.16.0'
    ],
    python_requires=">=3.8",
)
