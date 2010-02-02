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
    Functions for Email related tasks
    """
    def validateRFC(self, email):
        """
        Validate an e-mail address within <brackets>,
        the format conforming to RFC 2812.
        Return True or False
        """
        pattern = re.compile('^<[a-z0-9._]+\@[a-z0-9]+\.[a-z.]{2,5}>', re.I)
        if re.match(pattern, email): r = True
        else: r = False
        return r
