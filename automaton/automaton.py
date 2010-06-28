#!/usr/bin/python
"""
Automaton 
Scriptable host interaction client
Copyright (c) 2010 Sam Saint-Pettersen

Released under the MIT License.
"""
import sys
import os
import getopt
import socket
import signal
import threading
import cPickle
import datetime
import re
import Queue

class AIS_Command:
	pass
	
class AIS_Engine:
    """
    Script engine to execute commands in a script
    ('engine': One and only instance, used by script threads)
    """
    def parse(self, command):
        return 'a'
	
class ScriptThread(threading.Thread):
	"""
	Script thread to execute a script on host machine
	(May be more than one instance)
	"""	
	def __init__(self, conn, engine, debug, script):
	    """
	    Initialization method for script thread
	    """
	    self.debug = debug 
	    self.script = script
	    self.conn = conn
	    self.engine = engine
	    threading.Thread.__init__(self)
	
	def run(self):
		self.executeScript()
		
	def executeScript(self):
		print('Executing \'{0}\'...\n'.format(self.script))
		
		# Read script file line-by-line, parse each command in file
		self.engine.parse('pineapple')
		
		print('Done.')
		
class ConnectionThread(threading.Thread):
	"""
	Connection thread to connect to target host
    (One and only instance)
	"""
	def __init__(self, debug, host, port, script, Max_conc):
		"""
		Initialization method for connection thread
		"""
		self.debug = debug
		self.host = host
		self.port = port
		self.script = script
		self.Max_conc = Max_conc
		self.scriptPool = Queue.Queue(0)
		self.engine = AIS_Engine()
		threading.Thread.__init__(self)
		
	def run(self):
		self.connectQueue()
		
	def connectQueue(self):
		"""
		Connect to target host, parse scripts to execution and queue
		"""
		print('\nConnecting to {0}:{1}...'.format(self.host, self.port))
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect((self.host, self.port))
		# Establish connection session 
		for i, script in enumerate(self.script):
			# Execute a script thread for each script, but
			ScriptThread(s, self.engine, self.debug, script).start()
			if i > self.Max_conc:
				# ... queue scripts out of concurrent maximum
				self.scriptPool.put(script)
				
			# When concurrent scripts have been executed, pool remaining
			
		#s.close()
				
class Automaton:
	"""
	Automation instance class
	(One and only instance)
	"""
	def __init__(self):
		"""
		Initialization method for Automation
		"""
		# Application information
		self.Name = 'Automaton'
		self.Vers = '1.0'
		# 
		self.Max_conc = 5 # Maximum allowable concurrent scripts (5)
		self.host = 'localhost' # Host to default to ('localhost'/127.0.0.1)
		self.port = 8282 # Port number to default to (8282, no sudo)
		self.script = [] # Default script is blank
		self.termSig = False # Signal to terminate application, start false
		self.debug = False # Enable debugging, default as false
		
		# Handle command line options
		try:
			opts, args = getopt.getopt(sys.argv[1:],'h:p:s:t:vid')
			for o, a in opts:
				# Switches with arguments
				if o == '-h':
				    self.host = a
				elif o == '-p':
				    self.port = int(a)
				elif o == '-s':
					for s in a.split('+'): self.script.append(s)
				# Switches without arguments
				elif o == '-i':
					self.displayCmdLineOps()
				elif o == '-v':
				    self.displayInfo()
                #elif o == '-d':
                	#self.debug = True
		
		# For invalid command line options, show general error message			
		except getopt.GetoptError, err:
			print('\nError: {0}.'.format(err))
			self.displayCmdLineOps()
			
		# Specifically for an invalid port number, show more specific error message
		except ValueError:
			print('\nError: Port number must be unsigned integer value, not \'{0}\'.'.format(a))
			self.displayCmdLineOps()
		
		print(__doc__)
		print('Hold Ctrl-C to terminate.')
		ConnectionThread(self.debug, self.host, self.port, 
		self.script, self.Max_conc).start()
		while not self.termSig:
			signal.signal(signal.SIGINT, self.quit)
			if self.termSig: sys.exit(0)
					
	def displayCmdLineOps(self):
		"""
		Display command line options
		"""
		print(__doc__)
		print('Usage: {0} [-i][-v][-b][-c]'.format(sys.argv[0]) 
		+ '\n[-d -h <hostname> -p <port number> -s <script+(script+)> (-q)]\n')
		print('-i: Display this information and exit.')
		print('-v: Display version information and exit.')	
		print('-b: Display built-in commands.')
		print('-c: Display defined commands and variables.')
		print('-d: Display debug information while running.')
		print('-h: Hostname to connect to. (\'localhost\' if omitted)')
		print('-p: Listen on specified port number. (8282 if omitted)')
		print('-s: Script(s) to execute; *.ais file(s). (Mandatory arg)')
		print('-q: Queue each script, rather than execute 5 at a time.\n')
		sys.exit(0)

	def	displayInfo(self):
	    print('{0} {1} ({2}/{3})'.format(self.Name, self.Vers, sys.platform, os.name))
	    sys.exit(0)
		
	def quit(self, signum, frame):
		print('\nClient terminated.\n')
		self.termSig = True

if __name__ == '__main__': Automaton()
