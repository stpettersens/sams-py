"""
Echo server
"""
import socket

class EchoServer:
    def __init__(self, port=100):
        print(__doc__)  
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('', port))
        s.listen(1)
        conn, addr = s.accept()
        while True:
            chunk = conn.recv(1024)
            print(chunk)
            conn.send(chunk)
        conn.close()
        
if __name__ == '__main__': EchoServer()
