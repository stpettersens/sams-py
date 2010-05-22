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
import theading
import datetime
import re
import Queue

class Automation:
	def __init__(self):
		# Application information/settings
		self.Name = 'Automation'
		self.Desc = 'Scriptable host interaction tool'
		self.MAX_SCRIPTS = 5
		#
		
		# Handle command line options
		try:
			opts, args = getopt.getopt(sys.argv[1:],'h:p:s:vid')
			