#!/bin/env python
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

gdebug = False
gclientPool = 0
gclients = 0
        
class Info:
    def __init__(self):
        self.Name = 'SMTP server'
        self.Vers = '0.1'
        self.Greeting = '{0} v{1} on {2} \'{3}\''.format(self.Name, self.Vers, sys.platform, os.name)
        self.ExitMsg = '221 Goodbye\r\n'
        self.MAX_CONNECTIONS = 5

class SMTPCommand:        
    def __init__(self, state):
        self.state = state # Server state as relevant for executed command
        self.msgdata = '' # Message data is initially blank
        
    def invalidSeq(self):
        return '503 Invalid sequence of commands.\r\n'
        
    def helo(self, host=''):
        # Return the state and message (tuple array) for each SMTP command
        if host == '' and self.state == 1:
            r = (1, '501 HELO/EHLO requires a domain address\r\n')
        elif self.state != 1: r = (self.state, self.invalidSeq())
        else:
            r = (2, '250 Hello, {0}. Have a message to send?\r\n'.format(host))
        return r
        
    def ehlo(self, host=''):
        return self.helo(host)
        
    def mailfrom(self, sender=''):
        if sender == '' and self.state == 2:
            r = (2, '501 MAIL FROM: requires a sender address\r\n')
        elif self.state != 2: r = (self.state, self.invalidSeq())
        elif mod_sam.Email().validateRFC(sender) and self.state == 2:
            r = (3, '250 {0}... Sender OK\r\n'.format(sender))
        else:
            r = (2, '553 {0} does not conform to RFC 2812 syntax.\r\n'.format(sender))
        return r
        
    def rcptto(self, to=''):
        if to == '' and self.state == 3:
            r = (3, '501 RCPT TO: requires a recipient address\r\n')
        elif self.state != 3: r = (self.state, self.invalidSeq())
        elif mod_sam.Email().validateRFC(to) and self.state == 3:
            r = (4, '250 {0}... Recipient OK\r\n'.format(to))
        else:
            r = (3, '553 \'{0}\' does not conform to RFC 2812 syntax.\r\n'.format(to))
        return r
        
    def data(self, data=''):
        if data == '' and self.state == 4:
            r = (5, '354 Ready for message data; terminate with \'.\'\r\n')
        elif self.state < 4 or self.state > 5: r = (self.state, self.invalidSeq())
        else:
            self.msgdata += data
            r = (6, '250 Message body OK\r\n')
        return r
        
    def help(self):
        pass
        
    def rset(self):
        pass
        
    def quit(self):
        return (0, Info().ExitMsg)
        
    def unknown(self, command):
        return (self.state, '550 Unknown command: {0}\r\n'.format(command.upper()))
        
class ClientThread(threading.Thread):
    def __init__(self):
        self.state = 0
        threading.Thread.__init__(self)
        
    def run(self):
        self.handleClient()

    def handleClient(self):
        command = returned = ''
        global gclients
        while True:
            client = gclientPool.get()
            if client != None and self.state == 0 and gclients <= Info().MAX_CONNECTIONS:
                gclients += 1 # After connect, number of clients is one more
                client[0].send('220 {0} {1}\r\n'.format(Info().Greeting, datetime.datetime.now()))
                print('^ Client {0} connected. ({1}/{2}).'.format(client[1][0], gclients, Info().MAX_CONNECTIONS))
                self.state = 1 # Shift to ready state (1)
            while True and self.state >= 1:
                chunk = client[0].recv(1024)
                command += chunk
                # Wait for command termination characters (CR+LF) before continuing
                if command.endswith('\r\n'):
					self.state, returned = self.parseCommand(command)
					client[0].send(str(returned)) # Convert to string from tuple to not return internal state code
					# Debug: Received from  and response to client
					if gdebug:
					    print('\n<<< {0}'.format(command))
					    print('\n>>> {0}'.format(returned))
					command = ''
                if not chunk or returned == Info().ExitMsg: break
            client[0].close()
            gclients -= 1 # After disconnect, number of connected clients is one less
            
    def parseCommand(self, command):
        r = param = ''
        try:
            patt_noparams = re.compile('^[A-Z]{4}\r\n', re.I)
            patt_w1param = re.compile('^[A-Z]{4}\s*[\[\]A-Z0-9._]*\:*\s*[<>a-z0-9._@]*\r\n', re.I)
            if self.state == 5:
                r = SMTPCommand(5).data(command)
            elif re.match(patt_noparams, command):
                command = command.strip('\r\n')
                r = eval('SMTPCommand({0}).{1}()'.format(self.state, command.lower()))
            elif re.match(patt_w1param, command):
                command = command.strip('\r\n')
                if command.find(':') != -1:
                    command, param = command.split(':')
                    command = command.replace(' ', '')
                else:
                    command, param = command.split()
                param = param.strip()
                r = eval('SMTPCommand({0}).{1}(\'{2}\')'.format(self.state, command.lower(), param.lower()))
            
            else:
                r = SMTPCommand(self.state).unknown(command)
        except AttributeError:
            r = SMTPCommand(self.state).unknown(command)
        return r
        
class ServerThread(threading.Thread):
    def __init__(self, port):
        self.port = port
        threading.Thread.__init__(self)
    
    def run(self):
        self.listen()
        
    def listen(self):
        command = returned = ''
        print('\nListening on port {0}...\n'.format(self.port))
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('', self.port))
        s.listen(5)
        global gclientPool
        gclientPool = Queue.Queue(0) # Create client pool
        for x in xrange(Info().MAX_CONNECTIONS):
            ClientThread().start()
        while True:
            gclientPool.put(s.accept())

class SMTPServer:
    def __init__(self):
        self.termsig = False
        self.port = 25
                
        # Handle command line options
        try:
            opts, args = getopt.getopt(sys.argv[1:], 'vp:hd')
            for o, a in opts:
                if o == '-v':
                    self.displayInfo()
                elif o == '-p':
                    self.port = int(a)
                elif o == '-h':
                    self.displayCmdLineOps()
                elif o == '-d':
                    global gdebug
                    gdebug = True
                    
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
        print('Use switch -h for usage information.')
        if exit: sys.exit(2)
        
    def displayCmdLineOps(self):
        print(__doc__)
        print('Usage: {0} [-h][-v][-d -p <port number>]\n'.format(sys.argv[0]))
        print('-h: Display this information and exit.')
        print('-v: Display version information and exit.')
        print('-d: Display debug information while running.')
        print('-p: Listen on specified port number. (Default: 25)\n')
        sys.exit(2)
        
    def displayInfo(self):
        print(Info().Greeting)
        sys.exit(0)
        
    def quit(self, signum, frame):
        print('\nServer terminated.\n')
        self.termsig = True
    
if __name__ == '__main__': SMTPServer()
