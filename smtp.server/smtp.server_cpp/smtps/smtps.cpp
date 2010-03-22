/*
	Simple Mail Transport Protocol (SMTP) server
	Copyright (c) 2010 Sam Saint-Pettersen

	Port of original Python program to C++
	Core program released under the MIT License

	This program uses the following
	third party libraries (as licensed):
	* Boost.Asio (Boost License)
	* Boost.DateTime
	* Boost.Regex
	* Boost.System
	* Boost.Threading
	* Getopt (Public domain)
*/
#include <iostream>
#include <cstdlib>
#include <string>
#include "getopt.h"
//#include "boost/asio.hpp"
#include "boost/version.hpp"
using namespace std;

#define COMPILER "gcc"

bool gDebug = false;
int gClientPool = 0;
int gClients = 0;

void displayHeader();
void displayVersion();
void displayUsage();

class SMTPCommand {

};

class SMTPServer {
private:
	const string Name;
	const string Version;
	const string Greeting;
	const string ExitMsg;
	const int MaxConnections;
	float state;
public:
	float incrState() {
		state++;
		return state;
	}
	float decrState() {
		state--;
		return state;
	}
};

int main(int argc, char *argv[]) {
    bool termSig = false;
	int port = 25; // Port number to default to

	// Handle command line options
	char *pvalue = NULL;
	int c;
	try {
		while((c = getopt(argc, argv, "vhdp:")) != -1) {
			switch(c) {
				case 'v':
					displayVersion();
					break;
				case 'h':
					displayUsage();
					break;
				case 'd':
					gDebug = true;
					break;
				case 'p':
					pvalue = optarg;
					port = atoi(pvalue);
					if(port == 0) throw 1;
					break;
			}
		}
	}
	catch(int ex) {
		cout << argv[0] << ": port must be a positive integer value, not \'" 
		<< pvalue << "\'.\n";
		displayUsage();
	}
	displayHeader();
    cout << "\nRunning on port " << port << "...\n";

    return 0;
}
void displayHeader() {
    cout << "\nSimple Mail Transport Protocol (SMTP) server";
    cout << "\nCopyright (c) 2010 Sam Saint-Pettersen";
    cout << "\n\nReleased under the MIT License\n";
}
void displayVersion() {
	cout << "SMTP version 1.0 (" << COMPILER
	<< ") using Boost " << BOOST_LIB_VERSION << "\n";
	exit(2);
}
void displayUsage() {
    displayHeader();
    exit(2);
}
