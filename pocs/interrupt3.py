# Proof of concept: exit on interrupt using signal module
import sys
import signal

def quit(signal, frame):
    print('This is stupid...')
    sys.exit(0)
    
def test():
    signal.signal(signal.SIGINT, quit)
    i = 0
    while 1:
        print(i)
        i += 1        
test()
