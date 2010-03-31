/*
	Simple Mail Transport Protocol (SMTP) server
	Copyright (c) 2010 Sam Saint-Pettersen

	Port of original Python program to C++
	Core program released under the MIT License

	This program uses the following
	third party libraries (as licensed):
	* Boost.Asio (Boost License)
	* Boost.System
	* Boost.DateTime
	* Boost.Regex
	* Boost.Thread
	* Getopt (Public domain)
*/
#include <iostream>
#include <cstdlib>
#include "getopt.h"
#include "boost/bind.hpp"
#include "boost/shared_ptr.hpp"
#include "boost/enable_shared_from_this.hpp"
#include "boost/asio.hpp"
#include "boost/regex.hpp"
#include "boost/thread.hpp"
#include "boost/version.hpp"
using namespace std;
using boost::asio::ip::tcp;

#define COMPILER "gcc"

bool gDebug = false;

void displayHeader();
void displayVersion();
void displayUsage();
bool validateEmail(char *emailAddress);

class SMTPCommand {
private:
	float state; // FSM state in command
	char *msgdata; // Message data
	char *r; // Response from executed command
public:
	SMTPCommand(float st) { 
		msgdata, r = new char; // Allocate memory for msgdata and response
		// Server state as relevant for executed command
		state = st;
		// Message data is intially blank
		msgdata = NULL; //!
	}
	// Need destructor here...
	///
	///
	char *invalidSeq() {
		sprintf(r, "%1.1f|501 Invalid sequence of commands.\r\n.", state);
		return r;
	}
	char *helo(char *host) {
		if(host == " " && state == 1.0) {
			r = "1.0|501 HELO/ELHO requires a domain address\r\n";
		}
		else if(state != 1) {
			r = invalidSeq();
		}
		else {
			r = "2.0|250 Hello.\r\n";
		}
		return r;
	}
	char *ehlo(char *host) {
		return helo(host);
	}
	char *mailfrom(char *sender) {
		if(sender == NULL && state == 2.0) {
			r = "2.0|501 MAIL FROM: requires a sender address\r\n";
		}
		else if(state == 2.0) {
			r = invalidSeq();
		}
		else if(validateEmail(sender) && state == 2.0) {
			sprintf(r, "3.0|250 %s... Sender OK\r\n", sender);
		}
		else {
			sprintf(r, "2.0|553 %s does not conform to RFC 2812 syntax.\r\n", sender);
		}
		return r;
	}
	char *rcptto(char *to) {
		if(to == NULL && state < 5.0) {
			sprintf(r, "%1.1f|501 RCPT TO: requires a recipient address\r\n", state);
		}
		else if(state < 3 || state > 5) {
			r = invalidSeq();
		}
		else if(validateEmail(to) && state < 5) {
			if(state == 3) {
				state += 1.1;
				cout << "A!" << state; //!
			}
			else {
				state += 0.1;
				cout << "B!" << state; //!
			}
			sprintf(r, "%1.1f|250 %s... Recipient OK\r\n", 
			state, to);
		}
		else {
			sprintf(r, "%1.1f|553 '%s' does not conform to RFC 2812 syntax\r\n", 
			state, to);
		}
		return r;
	}
};

class Session {
private:
	tcp::socket socket_;
	enum { max_length = 1024 };
	char data_[max_length];
public:
	Session(boost::asio::io_service& io_service)
	: socket_(io_service) 
	{
	}
	tcp::socket& socket() {
		return socket_;
	}
	void start() {
		socket_.async_read_some(boost::asio::buffer(data_, max_length),
		boost::bind(&Session::handle_read, this, 
		boost::asio::placeholders::error,
		boost::asio::placeholders::bytes_transferred));
	}
	void handle_read(const boost::system::error_code &error, size_t bytes_transferred) {
		if(!error) {
			boost::asio::async_write(socket_,
				boost::asio::buffer(data_, bytes_transferred),
				boost::bind(&Session::handle_write, this, 
				boost::asio::placeholders::error));
		}
		else {
			delete this;
		}
	}
	void handle_write(const boost::system::error_code& error) {
		if(!error) {
			socket_.async_read_some(boost::asio::buffer(data_, max_length),
				boost::bind(&Session::handle_read, this, 
				boost::asio::placeholders::error,
				boost::asio::placeholders::bytes_transferred));
		}
		else {
			delete this;
		}
	}
};

class SMTPServer {
private:
	char *name;
	char *version;
	char *greeting;
	char *exitMsg;
	int maxConnections;
	int clientCount;
	float state;
	boost::asio::io_service& io_service_;
	tcp::acceptor acceptor_;
public:
	SMTPServer(boost::asio::io_service &io_service, int port)
		: io_service_(io_service), 
		acceptor_(io_service, tcp::endpoint(tcp::v4(), port))
	{

		maxConnections = 5; // Set maximum number of connections allowed
		clientCount = 0; // Intially there are no client connections
		state = 0.0; // Set initial FSM state to 0.00

		Session* new_session = new Session(io_service_);
		acceptor_.async_accept(new_session->socket(),
			boost::bind(&SMTPServer::handle_accept, this, new_session,
			boost::asio::placeholders::error));
	}
	void handle_accept(Session* new_session, const boost::system::error_code &error) {
		if(!error) {
			new_session->start();
			new_session = new Session(io_service_);
			acceptor_.async_accept(new_session->socket(),
				boost::bind(&SMTPServer::handle_accept, this, new_session,
				boost::asio::placeholders::error));
		}
		else {
			delete new_session;
		}
	}
	float incrState() {
		state++;
		return state;
	}
	float decrState() {
		state--;
		return state;
	}
	float returnState() {
		return state;
	}
};

bool validateEmail(char *emailAddress) {
	char *pattern = new char;
	return true;
}

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
		cerr << argv[0] << ": port must be a +ve integer value, not \'" 
		<< pvalue << "\'." << endl;
		displayUsage();
	}
	displayHeader();
	try {
		// Start SMTP server object on specified port
		cout << "\nRunning on port " << port << "..." << endl;
		boost::asio::io_service io_service;
		SMTPServer server(io_service, port);
		io_service.run();
	}
	catch(exception &e) {
		cerr << "Exception: " << e.what() << endl;
	}

	return 0;
}
void displayHeader() {
    cout << "\nSimple Mail Transport Protocol (SMTP) server" << endl;
    cout << "Copyright (c) 2010 Sam Saint-Pettersen" << endl;
    cout << "\nReleased under the MIT License" << endl;
}
void displayVersion() {
	cout << "SMTP version 1.0\nCompiled with " << COMPILER
	<< " using Boost " << BOOST_LIB_VERSION << endl;
	exit(2);
}
void displayUsage() {
    displayHeader();
    exit(2);
}
