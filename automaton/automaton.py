#!/usr/bin/python
"""
Automaton 
Scriptable host interaction tool
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

class Automaton:
	def __init__(self):
		# Application information
		self.Name = 'Automaton'
		self.Vers = '1.0'
		# 
		self.MAX_SCRIPTS = 5
		self.port = 8282 # Port number to default to (8282, no sudo)
		self.termSig = False
		
		# Handle command line options
		try:
			opts, args = getopt.getopt(sys.argv[1:],'h:p:s:q:t:vid')
			for o, a in opts:
				if o == '-h':
				    pass
				elif o == '-p':
				    self.port = int(a)
                # ... debugging ... 
					
		except getopt.GetoptError, err:
			print('\nError: {0}'.format(err))
			self.diplayUsage(True)
			
		except ValueError:
			print('\nError: Port must be an unsigned integer value, not \'{0}\''.format(a))
			self.displayUsage(True)
			
	def displayUsage(self, exit):
		print(__doc__)
		print('Use switch -i for usage information.')
		if exit: sys.exit(2)
		
	def displayCmdLineOps(self):
		print(__doc__)
		print('Usage: {0} [-i][-v][-h <hostname> -p <port number> -s <script, ....>'
		+ '-q <# scripts> -t <# threads >]\n'.format(sys.argv[0]))
		

if __name__ == '__main__': Automaton()
