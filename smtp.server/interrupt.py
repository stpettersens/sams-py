# Proof of concept: exit on interrupt using KeyboardInterrupt exception
import sys

def test():
    try:
        i = 0
        while i < 100000000:
            print(i)
            i += 1
    except KeyboardInterrupt:
        print('This is stupid...')
        sys.exit(0)
        
test()
