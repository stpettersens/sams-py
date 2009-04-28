# Command line structure:
# -h -f <filename> -l <line #> -m <word(s)> -r <word(s)>
switches, args = getopt.getopt(sys.argv[1:], "hqf:l:m:r:")

# When args are valid, perform appropriate action
for s, a in switches:
    if s == "-h": displayUsage() # With switch "-h", display usage
    if s == "-f": filename = a # With switch "-f", specify filename
    if s == "-l": lineNo = int(a) # With switch "-l", specify line no.
    if s == "-m": match = a # With switch "-m", specify match word(s)
    if s == "-r": repl = a # With switch "-r", specify replacement
    if s == "-q": verbose = False # With switch "-q", suppress output

# With necessary arguments, process file
if len(sys.argv) > 2:
    if filename != "":
        processFile(filename, lineNo, match, repl)
        