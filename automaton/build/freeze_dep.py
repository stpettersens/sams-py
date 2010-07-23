# Workaround for using JSON module in "frozen" program
# This does not need to be run directly, used by
# Freeze tool in Makefile:
# $(FREEZE) -o /temp $@ $?  
from encodings import hex_codec

