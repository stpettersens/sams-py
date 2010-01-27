"""
Simple Mail Transport Protocol (SMTP) server
Copyright (c) 2010 Sam Saint-Pettersen

Released under the MIT License
"""
import sys
import getopt
import socket
import signal
import threading
import datetime
import re

class SMTPCommand:
    def helo(self, host=''):
        SMTPServerSW().state = 1 
        if host == '':
            r = '501 HELO/EHLO requires a domain address\r\n'
        else:
            r = '250 Hello, {0}\r\n'.format(host)
        return r
        
    def ehlo(self, host=''): # Alias for HELO
        return self.helo(host)
        
    def mail(self, sender=''):
        SMTPServerSW().state = 2
        if sender == '':
            r = '501 MAIL FROM: requires a sender address\r\n'
        else:
            r = '250 Sender address is {0}\r\n'.format(sender)
        return r
        
    def rcpt(self, to=''):
        SMTPServerSW().state = 3
        if to == '':
            r = '501 RCPT TO: requires a receipient address\r\n'
        else:
            r = '250 Receipient address is {0}\r\n'.format(to)
        return r
        
    def data(self):
        pass
    
    def help(self):
        pass
        
    def rset(self):
        pass
        
    def quit(self):
        return SMTPServerSW().ExitMsg
        
    def unknown(self):
        return '550 Unknown command\r\n'
        
class SMTPServerSW(threading.Thread):
    def __init__(self):
        self.Name = 'SMTP server'
        self.Vers = '0.1'
        self.Greeting = '{0} v{1}'.format(self.Name, self.Vers)
        self.ExitMsg = '221 Goodbye\r\n'
        self.state = 0 # Start in waiting state (0)
        threading.Thread.__init__(self)
        
    def run(self):
        self.listen()
        
    def parseCommand(self, command):
        r = ''
        try:
            patt_noparams = re.compile('^[A-Z]{4}\r\n', re.I)
            patt_w1param = re.compile('^[A-Z]{4}\s*[A-Z._]*[A-Z]{0,4}\:*[A-Z._@]*\r\n', re.I)
            if re.match(patt_noparams, command):
                command = command.replace('\r\n', '')
                r = eval('SMTPCommand().{0}()'.format(command.lower()))
            elif re.match(patt_w1param, command):
                command = command.replace('\r\n', '')
                if command.find(':') != -1:
                    command, param = command.split(':')
                    command, junk = command.split()
                    del junk # Be a good command parser and throw away your unused junk data
                else:
                    command, param = command.split()
                r = eval('SMTPCommand().{0}(\'{1}\')'.format(command.lower(), param.lower()))  
            else:
                r = SMTPCommand().unknown()             
        except AttributeError:
            r = SMTPCommand().unknown()
        return r
        
    def listen(self, port=26): # Change to port 25 later
        command = returned = ''
        print('Listening on port {0}...\n'.format(port))
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('', port))
        s.listen(1)
        conn, addr = s.accept()
        while 1:
            if self.state == 0:
                date = datetime.datetime.now()
                # Relay connected information to client\
                conn.send('220 {0} {1}\r\n'.format(self.Greeting, date))
                print('>> {0} connected.\n'.format(addr))
                self.state = 1 # Shift to ready state (1)
            chunk = conn.recv(1024)
            command += chunk
            # Wait for command termination characters (CR+LF) before continuing
            if command.endswith('\r\n'):
                returned = self.parseCommand(command)
                conn.send(returned)
                command = ''
            if not chunk or returned == self.ExitMsg: break
        conn.close()
        
class SMTPServer:
    def __init__(self):
        self.control = 0 # Initiate server application run state (0)
        print(__doc__)
        print('Hold Ctrl-C to terminate.')
        SMTPServerSW().setDaemon(True) 
        SMTPServerSW().start()
        while self.control == 0:
            signal.signal(signal.SIGINT, self.quit)
            if self.control == 1: break
        sys.exit(0)
        
    def quit(self, signum, frame):
        print('Server terminated.')
        self.control = 1 # Change to application quit-ready state (1)
    
if __name__ == '__main__': SMTPServer()
