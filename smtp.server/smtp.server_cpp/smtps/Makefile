# ===
# Makefile for smtps 
# ===
# Requirements to build:
# * GNU C++ compiler and related tools (gcc, make et al)
# * Boost libraries (Asio, Regex, etc.)
# * MSYS (Win)
# * UPX
# * Windows SDK (for Winsock library - WS2_32.lib, MsWSock.lib)

TARGET = smtps

INCL_W = -I"C:\Dev\boost_1_42_0"
LIBS_W = -L"C:\Program Files\Microsoft SDKs\Windows\v6.0A\Lib" \
-L"C:\Dev\boost_1_42_0\stage\lib" \
-llibboost_system-mgw34-mt -llibboost_regex-mgw34-mt -llibboost_thread-mgw34-mt \
-lws2_32 -lmswsock

INCL_U = -I"/usr/include/boost_1_42_0"
LIBS_U = -L"/usr/lib/boost_1_42_02" -llibboost_system-gcc-mt-sd-1_42

make: 
	@echo Build $(TARGET) program
	@echo make win - build Windows executable
	@echo make unix - build Unix-like exectuable
	
test: server.cpp
	g++ $(INCL_W) server.cpp -o demo.exe $(LIBS_W)
	strip server.exe
	
testc: demo.exe
	rm demo.exe

win: $(TARGET).cpp
	@echo Building executable for Win...
	g++ $(INCL_W) $(TARGET).cpp -o t.exe $(LIBS_W)
	strip t.exe
	upx -9 -o $(TARGET).exe t.exe 
	rm t.exe
	@echo Done.
	
unix: $(TARGET).cpp
	@echo Building executable for Unix-like...
	g++ $(INCL_U) $(TARGET).cpp -o t
	strip t
	upx -9 -o $(TARGET) t
	rm t
	@echo Done.
	
clean:
	@echo Specify clean_w or clean_u

clean_w: $(TARGET).exe
	rm $(TARGET).exe

clean_u: $(TARGET)
	rm $(TARGET)
