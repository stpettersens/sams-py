"""
Echo server to test interrupts
"""
import sys
import socket

class EchoServer:
    def __init__(self, port=1200):
        print(__doc__)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('', port))
        s.listen(1)
        conn, addr = s.accept()
        try:
            while 1:
                chunk = conn.recv(1024)
                print(chunk)
                conn.send(chunk)
        # I want the server to terminate when Ctrl-C/Z is pressed
        except KeyboardInterrupt: 
            conn.close()
            sys.exit(0)
                
        conn.close()
        sys.exit(0)
        
if __name__ == '__main__': EchoServer()
