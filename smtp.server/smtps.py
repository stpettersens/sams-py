#!/usr/bin/python
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
import helpers # Non-PSL module

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
        
class Mailer:
    def __init__(self, msgdata):
        self.msgdata = msgdata
        self.sendMail()
        
    def log(self):
        timestamp = datetime.datetime.now()
        log = open('mail.log', 'a')
        log.write('\nMessage processed: {0}\n\n{1}\n'.format(timestamp, self.msgdata))
        log.close()
        
    def sendMail(self):
        self.log()
		     
class SMTPCommand:        
    def __init__(self, state):
        self.state = state # Server state as relevant for executed command
        self.msgdata = '' # Message data is initially blank
        
    def invalidSeq(self):
        return '503 Invalid sequence of commands.\r\n'
        
    def helo(self, host=''):
        # Return the state and message (tuple array) for each SMTP command
        if host == '' and self.state == 1.0:
            r = (1.0, '501 HELO/EHLO requires a domain address\r\n')
        elif self.state != 1: r = (self.state, self.invalidSeq())
        else:
            r = (2.0, '250 Hello, {0}. Have a message to send?\r\n'.format(host))
        return r
        
    def ehlo(self, host=''):
        return self.helo(host)
        
    def mailfrom(self, sender=''):
        if sender == '' and self.state == 2.0:
            r = (2.0, '501 MAIL FROM: requires a sender address\r\n')
        elif self.state != 2: r = (self.state, self.invalidSeq())
        elif helpers.Email().validateRFC(sender) and self.state == 2:
            r = (3.0, '250 {0}... Sender OK\r\n'.format(sender))
        else:
            r = (2.0, '553 {0} does not conform to RFC 2812 syntax.\r\n'.format(sender))
        return r
        
    def rcptto(self, to=''):
        if to == '' and self.state < 5.0:
            r = (self.state, '501 RCPT TO: requires a recipient address\r\n')
        elif self.state < 3.0 or self.state > 5.0: r = (self.state, self.invalidSeq())
        elif helpers.Email().validateRFC(to) and self.state < 5:
			if self.state == 3.0:
			    self.state += 1.1
			else: 
			    self.state += 0.1
			r = (self.state, '250 {0}... Recipient OK\r\n'.format(to))
        else:
            r = (self.state, '553 \'{0}\' does not conform to RFC 2812 syntax\r\n'.format(to))
        return r
        
    def data(self, data=''):
        if data == '' and self.state < 5.0:
            r = (5.0, '354 Ready for message data; terminate with \'.\'\r\n')
        elif self.state < 4 or self.state > 5.0: r = (self.state, self.invalidSeq())
        else:
            self.msgdata += data
            r = (6.0, '250 Message body OK\r\n')
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
        self.state = 0.0
        threading.Thread.__init__(self)
        
    def run(self):
        self.handleClient()

    def handleClient(self):
        command = returned = ''
        global gclients
        while True:
            client = gclientPool.get()
            if client != None and self.state == 0.0 and gclients <= Info().MAX_CONNECTIONS:
                gclients += 1 # After connect, number of clients is one more
                client[0].send('220 {0} {1}\r\n'.format(Info().Greeting, datetime.datetime.now()))
                print('^ Client {0} connected. ({1}/{2}).'.format(client[1][0], gclients, Info().MAX_CONNECTIONS))
                self.state = 1.0 # Shift to ready state (1.0)
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
					# After DATA finishes, send message
					if self.state == 6.0:
						Mailer(returned)
                if not chunk or returned == Info().ExitMsg: break
            client[0].close()
            gclients -= 1 # After disconnect, number of connected clients is one less
            
    def parseCommand(self, command):
        r = param = ''
        try:
            patt_noparams = re.compile('^[A-Z]{4}\r\n', re.I)
            patt_w1param = re.compile('^[A-Z]{4}\s*[\[\]A-Z0-9._]*\:*\s*[<>a-z0-9._@]*\r\n', re.I)
            if self.state == 5.0:
                r = SMTPCommand(5.0).data(command)
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
        self.port = 25 # Port number to default to (SMTP standard: 25)
        self.termSig = False
                
        # Handle command line options
        try:
            opts, args = getopt.getopt(sys.argv[1:], 'p:vid')
            for o, a in opts:
                if o == '-v':
                    self.displayInfo()
                elif o == '-p':
                    self.port = int(a)
                elif o == '-i':
                    self.displayCmdLineOps()
                elif o == '-d':
                    global gdebug
                    gdebug = True
                    
        except getopt.GetoptError, err:
            print('\nError: {0}'.format(err))   
            self.displayUsage(True)
            
        except ValueError:
            print('\nError: Port must be an unsigned integer value, not \'{0}\'.'.format(a))
            self.displayUsage(True)
                               
        self.displayUsage(False)
        print('\nHold Ctrl-C to terminate.')
        ServerThread(self.port).start()
        while not self.termSig:
            signal.signal(signal.SIGINT, self.quit)
            if self.termSig: break
        sys.exit(0)
        
    def displayUsage(self, exit):
        print(__doc__)
        print('Use switch -i for usage information.')
        if exit: sys.exit(2)
        
    def displayCmdLineOps(self):
        print(__doc__)
        print('Usage: {0} [-i][-v][-d -p <port number>]\n'.format(sys.argv[0]))
        print('-i: Display this information and exit.')
        print('-v: Display version information and exit.')
        print('-d: Display debug information while running.')
        print('-p: Listen on specified port number. (Default: 25)\n')
        sys.exit(2)
        
    def displayInfo(self):
        print(Info().Greeting)
        sys.exit(0)
        
    def quit(self, signum, frame):
        print('\nServer terminated.\n')
        self.termSig = True
    
if __name__ == '__main__': SMTPServer()
