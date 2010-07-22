# Create Windows executable for AUTOMATON using
# Py2Exe module - http://www.py2exe.org
# Usage: python create_exe.py py2exe
# Recommended: Use Makefile
from distutils.core import setup
import py2exe
import sys

setup(
    options = {'py2exe': {'bundle_files': 1}},
    console = ['automaton.py'],
    zipfile = None,
)
