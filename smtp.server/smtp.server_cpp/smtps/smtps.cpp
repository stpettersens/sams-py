/*
	Simple Mail Transport Protocol (SMTP) server
	Copyright (c) 2010 Sam Saint-Pettersen

	Port of original Python program to C++
	Core program released under the MIT License

	This program uses the following
	third party libraries by respective authors (as licensed):
	* Boost.Asio (Boost License)
	* Boost.DateTime
	* Boost.Regex
	* Boost.System
	* Boost.Threading
	* Getopt (Public domain)
*/
#include <iostream>
#include <string>
#include "getopt.h"
using namespace std;

bool gDebug = false;
int gClientPool = 0;
int gClients = 0;

void displayHeader();
void displayUsage();

class Info {
	
};

class SMTPCommand {

};

int main(int argc, char *argv[]) {
    bool termSig = false;
	int port = 25; // Port number to default to

	// Handle command line options
	int operror = 0;
	char *cvalue = NULL;
	int index, c;
	while((c = getopt(argc, argv, "vp:hd")) != -1) {
		switch(c) {
			case 'v':
				break;
			case 'p':
				cvalue = optarg;
				port = atoi(cvalue);
				break;
			case 'h':
                displayUsage();
                break;
            case 'd':
                gDebug = true;
                break;
			case '?':
				break;
        }
    }
    displayHeader();
    cout << "\n\nRunning on port " << port << "...\n";
        
    return 0;
}
void displayHeader() {
    cout << "\nSimple Mail Transport Protocol (SMTP) server";
    cout << "\nCopyright (c) 2010 Sam Saint-Pettersen";
    cout << "\n\nReleased under the MIT License";
}
void displayUsage() {
    displayHeader();
    exit(2);
}
