"""
Simple Mail Transport Protocol (SMTP) server
Copyright (c) 2010 Sam Saint-Pettersen

Released under the MIT License
"""
import sys
import os
import getopt
import socket
import signal
import threading
import datetime
import re
import Queue
import mod_sam # Non-PSL module; include with this code

gclients = 0
        
class RelayInfo:
    def __init__(self):
        self.Name = 'SMTP server'
        self.Vers = '0.1'
        self.Greeting = '{0} v{1} on {2} \'{3}\''.format(self.Name, self.Vers, sys.platform, os.name)
        self.ExitMsg = '221 Goodbye\r\n'

class SMTPCommand:
    def helo(self, host=''):
        # TODO: Return message and the state (array) for each SMTP command
        if host == '':
            r = '501 HELO/EHLO requires a domain address\r\n'
        else:
            r = '250 Hello, {0}. Have a message to send?\r\n'.format(host)
        return r
        
    def mailfrom(self, sender=''):
        if sender == '':
            r = '501 MAIL FROM: requires a sender address\r\n'
        elif mod_sam.Email().validateRFC(sender):
            r = '250 {0}... Sender OK\r\n'.format(sender)
        else:
            r = '553 {0} does not conform to RFC 2812 syntax.\r\n'.format(sender)
        return r
        
    def rcptto(self, to=''):
        if to == '':
            r = '501 RCPT TO: requires a recipient address\r\n'
        elif mod_sam.Email().validateRFC(to):
            r = '250 {0}... Recipient OK\r\n'.format(to)
        else:
            r = '553 \'{0}\' does not conform to RFC 2812 syntax.\r\n'.format(to)
        return r
        
    def data(self):
        pass
    
    def help(self):
        pass
        
    def rset(self):
        pass
        
    def quit(self):
        return RelayInfo().ExitMsg
        
    def unknown(self, command):
        return '550 Unknown command: {0}\r\n'.format(command.upper())
        
class ClientThread(threading.Thread):
    def __init__(self, conn, addr):
        self.conn = conn
        self.addr = addr
        self.MAX_CLIENTS = 5
        self.state = 0
        threading.Thread.__init__(self)
        
    def run(self):
        self.handleClient()

    def handleClient(self):
        command = returned = ''
        global gclients
        while True:
            if self.state == 0 and gclients <= self.MAX_CLIENTS:
                gclients += 1
                date = datetime.datetime.now()
                self.conn.send('220 {0} {1}\r\n'.format(RelayInfo().Greeting, date))
                print('>> Client {0} connected. ({1}/{2}).'.format(self.addr, gclients, self.MAX_CLIENTS))
                self.state = 1 # Shift to ready state (1)
            chunk = self.conn.recv(1024)
            command += chunk
            # Wait for command termination characters (CR+LF) before continuing
            if command.endswith('\r\n'):
                returned = self.parseCommand(command)
                self.conn.send(returned)
                command = ''
            if not chunk or returned == RelayInfo().ExitMsg: break
        print threading.enumerate() #self.conn.close()
        self.conn.close()
            
    def parseCommand(self, command):
        r = param = ''
        try:
            patt_noparams = re.compile('^[A-Z]{4}\r\n', re.I)
            patt_w1param = re.compile('^[A-Z]{4}\s*[A-Z0-9._]*\:*\s*[<>a-z._@]*\r\n', re.I)
            if re.match(patt_noparams, command):
                command = command.strip('\r\n')
                r = eval('SMTPCommand().{0}()'.format(command.lower()))
            elif re.match(patt_w1param, command):
                command = command.strip('\r\n')
                if command.find(':') != -1:
                    command, param = command.split(':')
                    command = command.replace(' ', '')
                else:
                    command, param = command.split()
                param = param.strip()
                r = eval('SMTPCommand().{0}(\'{1}\')'.format(command.lower(), param.lower()))  
            else:
                r = SMTPCommand().unknown(command)             
        except AttributeError:
            r = SMTPCommand().unknown(command)
        return r
        
class ServerThread(threading.Thread):
    def __init__(self, port):
        self.port = port
        threading.Thread.__init__(self)
    
    def run(self):
        self.listen()
        
    def listen(self):
        command = returned = ''
        global gport
        print('\nListening on port {0}...\n'.format(self.port))
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('', self.port))
        s.listen(5)
        while True:
            conn, addr = s.accept()
            ClientThread(conn, addr).start()

class SMTPServer:
    def __init__(self):
        self.termsig = False
        self.port = 25
                
        # Handle command line options
        try:
            opts, args = getopt.getopt(sys.argv[1:], 'vp:')
            for o, a in opts:
                if o == '-v':
                    self.displayInfo()
                elif o == '-p':
                    self.port = int(a)
                    
        except getopt.GetoptError, err:
            print('\nError: {0}'.format(err))   
            self.displayUsage(True)
            
        except ValueError:
            print('\nError: Port must be an integer value, not \'{0}\'.'.format(a))
            self.displayUsage(True)
                               
        self.displayUsage(False)
        print('\nHold Ctrl-C to terminate.')
        ServerThread(self.port).start()
        while not self.termsig:
            signal.signal(signal.SIGINT, self.quit)
            if self.termsig: break
        sys.exit(0)
        
    def displayUsage(self, exit):
        print(__doc__)
        print('Use switch -v for version information\nor -p <port> to set port.')
        if exit: sys.exit(2)
        
    def displayInfo(self):
        print(RelayInfo().Greeting)
        sys.exit(0)
        
    def quit(self, signum, frame):
        print('Server terminated.')
        self.termsig = True
    
if __name__ == '__main__': SMTPServer()
