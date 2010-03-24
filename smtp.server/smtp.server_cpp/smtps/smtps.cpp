/*
	Simple Mail Transport Protocol (SMTP) server
	Copyright (c) 2010 Sam Saint-Pettersen

	Port of original Python program to C++
	Core program released under the MIT License

	This program uses the following
	third party libraries (as licensed):
	* Boost.System
	* Boost.Asio (Boost License)
	* Boost.DateTime
	* Boost.Regex
	* Boost.Thread
	* Getopt (Public domain)
*/
#include <iostream>
#include <cstdlib>
#include "getopt.h"
#include "boost/asio.hpp"
#include "boost/regex.hpp"
#include "boost/thread.hpp"
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
private:
	float state;
	char *msgdata;
public:
	SMTPCommand(float st) {
		// Server state as relevant for executed command
		state = st;
		// Message data is intially blank
		msgdata = " ";
	}
private:
	char *invalidSeq(void) {
		return strcat("1", "|503 Invalid sequence of commands.\r\n");
	}
	char *helo(char *host) {
		char *r;
		if(host == " " && state == 1.0) {
			r = "1.0|501 HELO/ELHO requires a domain address.\r\n";
		}
		else if(state != 1) r = invalidSeq();
		else r = "2.0|250 Hello.\r\n";
		return r;
	}
	char *ehlo(char *host) {
		return helo(host);
	}
};

class SMTPServer {
private:
	char *name;
	char *version;
	char *greeting;
	char *exitMsg;
	char *maxConnections;
	float state;
public:
	SMTPServer() {
		state = 0;
	}
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
		cout << argv[0] << ": port must be a +ve integer value, not \'" 
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
	cout << "SMTP version 1.0\nCompiled with " << COMPILER
	<< " using Boost " << BOOST_LIB_VERSION << "\n";
	exit(2);
}
void displayUsage() {
    displayHeader();
    exit(2);
}
