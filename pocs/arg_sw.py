# Use a Python dictionary
# with command line options and arguments

import sys, getopt

def doSomething():
    print('I just did something')
    
values = ({
		'-h': 'localhost', #host 
		'-p': 8282, #port
		'-d': 'doSomething()' #doSomething()
		})
		
opts, args = getopt.getopt(sys.argv[1:],'h:p:d')
for o, a in opts:
    if a != '': 
        values[o] = a
        x = values.get(o)
        print(x)
    else:
        eval(values.get(o))
