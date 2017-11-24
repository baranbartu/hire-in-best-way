#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
from setuptools import setup, find_packages
from pnoa import __version__

README = open(os.path.join(os.path.dirname(__file__), 'README.md')).read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='pnoa',
    version=__version__,
    description='Predict number of applicants training existing data',
    long_description=README,
    author='Baran Bartu Demirci',
    author_email='bbartu.demirci@gmail.com',
    packages=find_packages(),
    entry_points={
        'console_scripts': ['pnoa = pnoa:init']
    },
    install_requires=[
        'numpy==1.13.3',
        'pandas==0.21.0',
        'scipy==1.0.0',
        'scikit-learn==0.19.1',
    ]
)
