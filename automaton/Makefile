#
# Makefile for automation 
#
# Requirements to build on Unix-like systems:
# * Make tool (e.g. GNU Make)
# * GNU C Compiler [GCC] 
# * Python 2.6.4/2.7
# * Freeze tool 
# * UPX (to compress executable)
#

TARGET = automaton
UPX = /usr/bin/upx
FREEZE = /usr/local/lib/python2.7/Tools/freeze/freeze.py
MAKE = /usr/bin/make
PYTHON = /usr/local/bin/python
BDIR= temp/

make: $(TARGET)

$(TARGET): $(TARGET).py
	$(PYTHON) $(FREEZE) -o $(BDIR)  $? build/freeze_dep.py
	$(MAKE) -C $(BDIR) -f Makefile
	mv $(BDIR)$@ $(BDIR)t
	$(UPX) -9 -o $@ $(BDIR)t
	rm -f $(BDIR)t
		
install: $(TARGET)
	cp $? /usr/bin 

clean:
	rm -f -r temp
