#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
from setuptools import setup, find_packages
from pnoa import __version__

README = open(os.path.join(os.path.dirname(__file__), 'README.md')).read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

version = '0.0.1'

setup(
    name='pnoa',
    version=__version__,
    description='Predict number of applicants training existing data',
    long_description=README,
    url='https://github.com/baranbartu/hire-in-best-way/predictnumberofapplicants',
    download_url='https://github.com/baranbartu/hire-in-best-way/predictnumberofapplicants/tarball/%s' % version,
    author='Baran Bartu Demirci',
    author_email='bbartu.demirci@gmail.com',
    packages=find_packages(),
    entry_points={
        'console_scripts': ['pnoa = pnoa.cli:main']
    },
    install_requires=[]
)
