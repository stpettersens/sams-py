"""
Simple Mail Transport Protocol (SMTP) server
As implemented in Python
Copyright (c) 2010 Sam Saint-Pettersen

Released under the MIT License
"""
import sys
import getopt

class AppInfo():
    def __init__(self):
        self.name = 'SMTP server'
        self.version = '0.1'
        self.language = 'en'
        
def main():
    """
    Main method
    """
    displayUsage() # !

def displayUsage():
    """ 
    Display usage information
    """
    print('\n' + __doc__)
    
# Invoke main method on run
if __name__ == '__main__': sys.exit(main())
