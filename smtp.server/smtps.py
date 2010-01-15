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
    listen()

def listen():    
    """
    Listen for and handle SMTP commands
    """
    PORT = 25
    print('Listening on port %d...' % PORT)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', PORT))
    s.listen(1)
    conn, addr = s.accept()
    while 1:
        data = conn.recv(4096)
        if data.endswith('\n'):
            print(data)
        
        if not data: break
        #conn.send(data)
   
    conn.close()

# Invoke main method on run
if __name__ == '__main__': sys.exit(main())
