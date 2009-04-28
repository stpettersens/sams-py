"""
Txtrevise
Command line text editing tool
Version 1.1
Copyright (c) 2009 Sam Saint-Pettersen

Released under the MIT License

IronPython port: Uses Rodger Aiken's
GPL-licensed CpGetOpt for .NET assembly
as IronPython Studio does not seem to 
support building executables with non 
IP built-in modules such as getopt and 
PYC produces messy executables. 
http://is.gd/tjHm
"""
import sys
import re
import clr
clr.AddReference("CpGetOpt")
from CodePoints import GetOpt 
from System import Array

version = '1.1ip' # Application version

def main():
    """
    Main method
    """
    # Produce verbose output by default
    global verbose; verbose = True
    
    # Count arguments provided, if none;
    # display "No arguments.." message and usage
    if len(sys.argv) < 2:
        displayError("No options specified")

    # Process provided arguments
    filename = match = repl = "(none)"
    lineNo = 1; i = 0
    swLst = "hqf:l:m:r:"
    
    # TODO: Somehow convert sys.argv (list) into an Array
 
    #try:
        #
        # Command line structure:
        # -h -f <filename> -l <line #> -m <word(s)> -r <word(s)>
        #while GetOpt.GetOptions(options, swLst) != 1:
	        #c = GetOpt.GetOptions(options, swList)

    # On exception(s), display an error message and usage
    #except ValueError:
        #displayError("Line number must be an integer")

def processFile(filename, lineNo, match, repl):
    """
    Process file
    @param filename File to read/write
    @param lineNo Line number to read
    @param match Word(s) to look for
    @param repl Replacement word(s) for match(es)
    """
    lineNum = index = 0
    allLines = []
    selLine = ""
    try:
        # Read each line in file sequentially, store selected line no
        f = open(filename, "r+") # r+: open for reading and writing
        for line in f:
            allLines.append(line)
            if lineNum == lineNo - 1: # - 1, because lines start at 0
                selLine = line
                index = lineNum
            lineNum += 1
                
        # Revise the selected line
        allLines[index] = matchReplace(selLine, lineNo, match, repl)
        f.seek(0) # Go to beginning of file to overwrite contents
        f.writelines(allLines) # Write all lines out to file
        f.close() # Close file

    # On I/O related exception, display an error message and usage
    except IOError:
        displayError("Invalid filename or permissions")
        
def matchReplace(line, lineNo, match, repl):
    """
    Match and replace word(s)
    @param line Line with matched word(s) to replace
    @param lineNo Line number to to do match and replace on
    @param match Word(s) to match
    @param repl Word(s) to replace match(es) with
    @return newLine Edited line
    """
    # If word(s) are matched, return edited line with replacement word(s)
    if re.search(match, line):    
        if verbose: print("\nMatched at Line %d: %s" % (lineNo, line))
        newLine = re.sub(match, repl, line)
        if verbose: print("Replaced with:\t %s" % newLine)

    # Otherwise, return same line as before
    else:
        if verbose: print("\nNo matches at Line %d." % lineNo)
        newLine = line

    return newLine

def displayUsage():
    """
    Display usage information
    """
    print("\nTxtrevise v %s (%s)" % (version, sys.platform))
    print("Command line text editing tool")
    print("Copyright (c) 2009 Sam Saint-Pettersen")
    print("\nReleased under the MIT License")
    print("\nUsage: txtrevise [-h] (-q) -f <file> -l <line #> -m <word(s)>")
    print("\t-r <word(s)>")
    print("\n\t-f: File to edit")
    print("\t-l: Line number to edit text on (starts at 1)")
    print("\t-m: Word(s) to match")
    print("\t-r: Replacement word(s) for matched word(s)")
    print("\t-q: Quiet mode. Only output to console for errors")
    print("\t-h: This help information")
    sys.exit(0)

def displayError(err):
    """
    Display an error message and usage instructions
    @param err Error to display in error message
    """
    print("\nError: %s." % err)
    displayUsage()

# Invoke main method
main()

