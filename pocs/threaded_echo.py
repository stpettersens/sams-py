"""
Threaded echo server
Proof-of-concept
Hold down Ctrl+C to quit
"""
import sys
import socket
import threading
import signal

control = 0
class EchoServerAttribs():
    def __init__(self):
        self.name = 'Echo server'

class EchoServer(threading.Thread):
    def run(self):
        print(__doc__)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('', int(sys.argv[1])))
        s.listen(1)
        channel, details = s.accept()
        while True:
            chunk = channel.recv(1024)
            print(chunk)
            print channel
            print details
            channel.send('Thanks for your data!')
            break
        channel.close()
        quit()

def quit():
    print('\n{0} terminated.'.format(EchoServerAttribs().name))
    global control
    control = 1

def quit_handler(signum, frame):
    quit()

EchoServer().setDaemon(True)
EchoServer().start()
while control == 0:
    signal.signal(signal.SIGINT, quit_handler)
    if control == 1: break
sys.exit(0)
