# Create Windows executable for %PROGRAM% using
# Py2Exe module - http://www.py2exe.org
# Usage: python create_exe.py py2exe
from distutils.core import setup
import py2exe
import sys

setup(
    options = {'py2exe': {'bundle_files': 1}},
    console = ['${0}'.format(sys.argv[1])],
    zipfile = None,
)
