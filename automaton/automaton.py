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
import datetime
import re
import Queue

class AIS_Command:
	pass
	
class AIS_Engine:
	pass
	
class ScriptThread(threading.Thread):
	"""
	Script thread to execute a script on host machine
	(May be more than one instance)
	"""
	pass

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
		threading.Thread.__init__(self)
		
	def run(self):
		self.connect()
		
	def connect(self):
		"""
		Connect to target host
		"""
		print('\nConnecting to {0}:{1}...'.format(self.host, self.port))
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect((self.host, self.port))
		# ... Establish connection session dohickey
		for i, s in enumerate(self.script):
			#... script execution thread
			ScriptThread(s).start()
			if i > Max_conc: 
				# ... queue remaining scripts (that is, its index (i))
	
		
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
		sys.exit(1)

	def	displayInfo(self):
		pass
		
	def quit(self, signum, frame):
		print('\nClient terminated.\n')
		self.termSig = True

if __name__ == '__main__': Automaton()
