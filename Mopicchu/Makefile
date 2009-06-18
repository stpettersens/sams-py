#
#	Makefile for MoPicchu
#
# THIS NEEDS ALTERED, NOT READY

COMPONENT = MoPicchu
FIREFOX_DIR = C:\Program Files\Mozilla Firefox
GECKOSDK_DIR = C:\dev\gecko-sdk

make:
	@echo nmake stack /f $(COMPONENT).mak - to build as stack
	@echo nmake queue /f $(COMPONENT).mak - to build as queue
	@echo nmake generate /f $(COMPONENT).mak - generate header and typelib for XPCOM
	@echo nmake autoreg /f $(COMPONENT).mak - when first registering component
	@echo nmake register /f $(COMPONENT).mak - register component with Firefox
	@echo nmake clean /f $(COMPONENT).mak - remove files created during building
	@echo nmake remove /f $(COMPONENT).mak - remove component from Firefox
	
stack:
	devenv $(COMPONENT).sln /build Release /project $(COMPONENT).vcproj /projectconfig Release
	@echo Built $(COMPONENT) as stack
	
queue:
	copy $(COMPONENT).sln $(COMPONENT)Queue.sln
	copy $(COMPONENT).vcproj $(COMPONENT)Queue.vcproj
	copy $(COMPONENT).cpp $(COMPONENT)Queue.cpp
	revise -f $(COMPONENT)Queue.sln -l 4 -m $(COMPONENT).vcproj -r $(COMPONENT)Queue.vcproj
	revise -f $(COMPONENT)Queue.vcproj -l 185 -m $(COMPONENT).cpp -r $(COMPONENT)Queue.cpp
	revise -f $(COMPONENT)Queue.cpp -l 75 -m Stack -r Queue
	devenv $(COMPONENT)Queue.sln /build Release /project $(COMPONENT)Queue.vcproj /projectconfig Release
	del $(COMPONENT)Queue.*
	@echo Built $(COMPONENT) as queue
	
generate:
	$(GECKOSDK_DIR)\bin\xpidl -m header -I$(GECKOSDK_DIR)\idl I$(COMPONENT).idl
	$(GECKOSDK_DIR)\bin\xpidl -m typelib -I$(GECKOSDK_DIR)\idl I$(COMPONENT).idl
	@echo Generated header and typelib for $(COMPONENT)
	
autoreg:
	copy /Y .autoreg "$(FIREFOX_DIR)"
	@echo Copied .autoreg file to allow component registration
	
register:
	touch -m "$(FIREFOX)\.autoreg"
	copy /Y Release\$(COMPONENT).dll "$(FIREFOX_DIR)\components"
	copy /Y I$(COMPONENT).xpt "$(FIREFOX_DIR)\components"
	$(GECKOSDK_DIR)\bin\regxpcom -x "$(FIREFOX_DIR)\components"
	@echo Registered $(COMPONENT)

clean:
	devenv $(COMPONENT).sln /clean Release /project $(COMPONENT).vcproj /projectconfig Release
	
remove:
	del "$(FIREFOX_DIR)\components\$(COMPONENT).dll"
	del "$(FIREFOX_DIR)\components\I$(COMPONENT).xpt"
	@echo Removed $(COMPONENT)
