# Create Windows executable for txtrevise
# Usage: python setup_exe.py py2exe
from distutils.core import setup
import py2exe

setup(
    options = {'py2exe': {'bundle_files': 1}},
    console = ['txtrevise.py'],
    zipfile = None,
)

