"""
Simple Mail Transport Protocol (SMTP) server
Copyright (c) 2010 Sam Saint-Pettersen

Released under the MIT License
"""
import sys
import getopt
import socket
#import signal
import datetime
import re
        
class SMTPCommand:
    def helo(self):
        # ...
        return '250 OK\r\n'
        
    def quit(self):
        pass
        
    def unrecognised(self):
        pass

class SMTPServer:
    def __init__(self):
        self.Name = 'SMTP server'
        self.Vers = '0.1'
        self.Greeting = '{0} v{1}'.format(self.Name, self.Vers)
        self.ExitMsg = 'Goodbye.\r\n'
        self.state = 0 # Start in listen state (0)
        print(__doc__)
        self.listen()
        
    def parseCommand(self, received):
        command = '' #!
        return 'blah' #!
        
    def listen(self, port=26): # Change to port 25 later
        received = returned = ''
        print('Listening on port {0}...\n'.format(port))
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('', port))
        s.listen(1)
        conn, addr = s.accept()
        while 1:
            if self.state == 0:
                date = datetime.datetime.now()
                # Relay connected information to client
                conn.send('220 {0} {1}\r\n'.format(self.Greeting, date))
                print('>> {0} connected.\n'.format(addr))
                self.state = 1 # Shift to ready state (1)
            chunk = conn.recv(1024)
            received += chunk
            # Wait for command termination characters (CR+LF) before continuing
            if received.endswith('\r\n'):
                print('>> {0}'.format(received))
                returned = self.parseCommand(received)
                print('<< {0}'.format(returned))
                conn.send(returned)
                received = ''
            if not chunk or returned == self.ExitMsg : break
        conn.close()
       
if __name__ == '__main__': SMTPServer()
