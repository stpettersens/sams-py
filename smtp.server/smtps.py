"""
Simple Mail Transport Protocol (SMTP) server
As implemented in Python
Copyright (c) 2010 Sam Saint-Pettersen

Released under the MIT License
"""
import sys
import getopt
import socket
import re

def main():
    """
    Main method
    """
    print(__doc__)
    
    
# Invoke main method on run
if __name__ == '__main__': sys.exit(main())
