"""
Simple Mail Transport Protocol (SMTP) server
Copyright (c) 2010 Sam Saint-Pettersen

Released under the MIT License
"""
import sys
import getopt
import socket
import re

class SMTPCommand:
    def helo(self):
        return '250 OK'

def main():
    print(__doc__)
    listen()

def listen(port=25):    
    cmd = ''
    print('Listening on port %d...' % port)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', port))
    s.listen(1)
    conn, addr = s.accept()
    while 1:
        data = conn.recv(1024)
        cmd += data  
        # Wait for command termination character: <CRLF> before processing
        if cmd.endswith('\r\n'): 
            print('>> %s' % cmd)
            cmd = SMTPCommand()
            print('<< %s' % cmd.helo())
            conn.send(cmd.helo())
            cmd = ''
        if not data: break
    conn.close()

# Invoke main method on run
if __name__ == '__main__': sys.exit(main())
