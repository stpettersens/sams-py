"""
Threaded echo server
Proof-of-concept
Hold down Ctrl+C to quit
"""
import sys
import socket
import threading
import signal

class EchoServer(threading.Thread):
    def run(self):
        print(__doc__)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('', 2727))
        s.listen(1)
        channel, details = s.accept()
        while True:
            print(channel.recv(1024))

def quit(signum, frame):
    sys.exit(0)

EchoServer().start()
while True:
    signal.signal(signal.SIGINT, quit)
