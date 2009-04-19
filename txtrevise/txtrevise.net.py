"""
Txtrevise
Command line text editing tool
Version 1.0
Copyright (c) 2009 Sam Saint-Pettersen

Released under the MIT License

Modified original for compatibility
with .NET (IronPython)

For now uses Rodger Aiken's LGPL
licensed GetOpt for .NET instead of
getopt module which for some reason does not work
"""
import sys
import re

version = '1.0' # Application version

def main():
    """
    Main method
    @return 0 exit code for application
    """
    # Count arguments provided, if none;
    # display "No arguments.." message and usage
    if len(sys.argv) < 2:
        displayError("No arguments specified")

    # Process provided arguments
    filename = match = repl = "(none)"
    lineNo = 1
    try:      
        # -h -f <filename> -l <line #> -m <word(s)> -r <word(s)>
        #switches = GetOpt.GetOptions(sys.argv[1:], "hvf:l:m:r:")

        # When args are valid, perform appropriate action
        #for s, a in switches:
            #if s == "-h": displayUsage() # With switch "-h", display usage
            #if s == "-f": filename = a # With switch "-f", specify filename
            #if s == "-l": lineNo = int(a) # With switch "-l", specify line no.
            #if s == "-m": match = a # With switch, "-m", specify match word(s)
            #if s == "-r": repl = a # With switch, "-r", specify replacement

        # With necessary arguments, read in file
        if len(sys.argv) > 2:
            if sys.argv[2] == filename:
                processFile(filename, lineNo, match, repl)

    # On exception(s), display an error message and usage
    except getopt.GetoptError, eMsg:
        displayError(eMsg)

    except ValueError:
        displayError("Line number must be an integer")

	return 0

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
            if lineNum == lineNo - 1: # because lines start at 0
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
    @param match Word(s) to match
    @param repl Word(s) to replace match(es) with
    @return newLine Edited line
    """
    # If word(s) are matched, return edited line with replacement word(s)
    if re.search(match, line):    
        print("\nMatched at Line %d: %s" % lineNo,line)
        newLine = re.sub(match, repl, line)
        print("Replaced with:\t %s" % newLine)

    # Otherwise, return same line as before
    else:
        print("\nNo matches at Line %d." % lineNo)
        newLine = line

    return newLine

def displayUsage():
    """
    Display usage information
    """
    print("\nTxtrevise v %s" % version)
    print("Command line text editing tool")
    print("Copyright (c) 2009 Sam Saint-Pettersen")
    print("\nReleased under the MIT License")
    print("\nUsage: txtrevise [-h] -f <file> -l <line #> -m <word(s)>")
    print("\t-r <word(s)>")
    print("\n\t-f: File to edit")
    print("\t-l: Line number to edit text on (starts at 1)")
    print("\t-m: Word(s) to match")
    print("\t-r: Replacement word(s) for matched word(s)")
    print("\t-h: This help information")

def displayError(err):
    """
    Display an error message and usage instructions
    @param err Error to display in error message
    """
    print("\nError: %s." % err)
    displayUsage()

# Invoke main method
main()
