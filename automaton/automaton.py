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

class Automaton:
	def __init__(self):
		# Application information
		self.Name = 'Automaton'
		self.Vers = '1.0'
		# 
		self.MAX_SCRIPTS = 5 # Maximum allowable concurrent scripts (5)
		self.host = 'localhost' # Host to default to ('localhost')
		self.port = 8282 # Port number to default to (8282, no sudo)
		self.script = [] # Default script is blank
		self.termSig = False
		
		# Handle command line options
		try:
			opts, args = getopt.getopt(sys.argv[1:],'h:p:s:t:vid')
			for o, a in opts:
				if o == '-h':
				    self.host = a
				elif o == '-p':
				    self.port = int(a)
				elif o == '-s':
					for x in a.split('+'): self.script.append(x)
				elif o == '-i':
					self.displayCmdLineOps()
                # ... debugging ... 
					
		except getopt.GetoptError, err:
			print('\nError: {0}.'.format(err))
			self.displayCmdLineOps()
			
		except ValueError:
			print('\nError: Port must be an unsigned integer value, not \'{0}\'.'.format(a))
			self.displayCmdLineOps()
					
	def displayCmdLineOps(self):
		print(__doc__)
		print('Usage: {0} [-i][-v][-b][-c]'.format(sys.argv[0]) 
		+ '\n[-d -h <hostname> -p <port number> -s <script+(script+)> -t <# threads >]\n')
		print('-i: Display this information and exit.')
		print('-v: Display version information and exit.')	
		print('-b: Display built-in commands.')
		print('-c: Display defined commands and variables.')
		print('-d: Display debug information while running.')
		print('-h: Hostname to connect to. (\'localhost\' if omitted)')
		print('-p: Listen on specified port number. (8282 if omitted)')
		print('-s: Script(s) to run; *.ais file(s). (Mandatory arg)')
		print('-t: Number of script threads to run concurrently on hosts. (<= 5)\n')
		sys.exit(2)

if __name__ == '__main__': Automaton()
