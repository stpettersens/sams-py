rm smtps.exe
g++ smtps.cpp -o t.exe
strip t.exe
upx -9 -o smtps.exe t.exe
rm t.exe


