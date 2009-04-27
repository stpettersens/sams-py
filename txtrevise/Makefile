# ===
# Makefile for txtrevise
# ===
# Requirements to build:
# * Python
# * Py2exe (Win) or Freeze (Unix)
# * MSYS (Win)
# * UPX

TARGET = txtrevise
INSTALL_DIR_W = /c/dev/bin # Change as desired

make:
	@echo
	@echo make py2exe - build + install py2exe executable
	@echo make freeze - build + install Freeze Unix exectuable

py2exe:
	@echo
	@echo Building executable...
	python create_exe.py py2exe
	rm -r build
	rm dist/w9xpopen.exe
	mv dist/${TARGET}.exe dist/t.exe
	upx -9 -o dist/${TARGET}.exe dist/t.exe
	rm dist/t.exe
	@echo Installing executable...
	mv dist/${TARGET}.exe ${INSTALL_DIR_W}
	@echo Done.
	
freeze:
	#TODO

