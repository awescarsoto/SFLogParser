__author__ = 'oxsc'

from distutils.core import setup
from glob import glob
import py2exe

data_files = [("Microsoft.VC90.CRT", glob(r'C:\Users\oxsc\Desktop\Programs\Calibre Portable\Calibre\Microsoft.VC90.CRT\*.*'))]
setup(data_files=data_files, console=['Parser.py'])
