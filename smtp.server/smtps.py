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

class SMTPServer:
    def __init__(self):
        print(__doc__)
        self.listen()
        
    def parseCommand(self, received):
        return '250 OK'
        
    def listen(self, port=25):
        received = ''
        print('Listening on port %d...\n' % port)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('', port))
        s.listen(1)
        conn, addr = s.accept()
        while True:
            chunk = conn.recv(1024)
            received += chunk
            if received.endswith('\r\n'): 
                print('>> %s' % received)
                returned = self.parseCommand(received)
                print('<< %s' % returned)
                conn.send(returned)
                received = ''
            if not chunk: break
        conn.close()

if __name__ == '__main__': SMTPServer()
