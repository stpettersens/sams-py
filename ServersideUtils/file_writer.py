"""
File writer utility (Python/mod_python implementation) 

Dynamically write files from provided data to a server cache.
 
Call with this URL with a returning Ajax request:
http://[your.server]/[path.to]/file_writer.py?out=
[output.path.relative.to.htdocs.dir]&data=[raw.encoded.data.to.write]
(&ext=[file.extension])

Copyright (c) 2009 Sam Saint-Pettersen.
 
Released under the MIT license.

This was tested with Apache 2.2.11 (Win32) w/ mod_python 3.3.1
using Python 2.5.4. The uuid module was introduced in Python 2.5,
so you will need at least that version to use this utility.
"""
from mod_python import apache
import uuid

def index(out='', data='', ext='txt'):
    """
    fileWriter function (named 'index' so that mod_python executes it)
    """
    # Generate UUID suffix for file
    nuuid = uuid.uuid4()
    # All options are required, except file extension;
    # which will use *.txt if not specified
    if(out != '' or data != ''):
        nfile = 'htdocs/' + out + '_' + str(nuuid) + '.' + ext 
        f = open(nfile, 'w')
        f.write(data);
        f.close();
        # Return relative path (w/o htdocs) to file to calling code
        return nfile.replace('htdocs', '')
    # Otherwise, return insufficient parameters message to calling code
    else: return 'Error: Insufficient parameters given.'
