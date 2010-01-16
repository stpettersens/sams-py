"""
Simple Mail Transport Protocol (SMTP) server
Copyright (c) 2010 Sam Saint-Pettersen

Released under the MIT License
"""
import getopt
import socket
import datetime
import re
        
class AppInfo:
    def __init__(self):
        self.name = 'SMTP server'
        self.vers = '0.1'
        self.greet = '{0} v{1}'.format(self.name, self.vers)
        
class SMTPCommand:
    def helo(self):
        return '250 OK'

class SMTPServer:
    def __init__(self):
        print(__doc__)
        self.state = 0
        self.listen()
        
    def parseCommand(self, received):
        
    def listen(self, port=26):
        received = ''
        print('Listening on port {0}...\n'.format(port))
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('', port))
        s.listen(1)
        conn, addr = s.accept()
        while True:
            if self.state == 0:
                date = datetime.datetime.now()
                conn.send('220 {0} {1}\r\n'.format(AppInfo().greet, date))
                print('>> 220 Client connected.\n')
                self.state += 1
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
