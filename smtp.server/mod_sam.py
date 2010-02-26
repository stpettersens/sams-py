"""
mod_sam

Module with useful classes and functions for Python programming

Copyright (c) 2010 Sam Saint-Pettersen

Released under the MIT License

Usage: import mod_sam
"""
import re

class Email:
    """
    Class for Email related tasks
    """
    def __init__(self):
        self.pattern = '[a-z0-9._]+\@[a-z0-9]+\.[a-z.]{2,5}'
        
    def validate(self, email):
        """
        Validate an e-mail address
        Return True or False
        """
        pattern = re.compile(self.pattern, re.I)
        if re.match(pattern, email): r = True
        else: r = False
        return r
        
        
    def validateRFC(self, email):
        """
        Validate an e-mail address within <brackets>,
        the format conforming to RFC 2812.
        Return True or False
        """
        self.pattern = '<' + self.pattern + '>'
        r = self.validate(email)
        return r
