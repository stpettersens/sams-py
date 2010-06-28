"""
Demonstrate Pickle module
with an application to pickle and unpickle an array of integers.
"""
import cPickle # Use C written version, faster

def showError():
    print('You must enter either 1 or 2!')

def doPickle():
    myIntegers = []
    for i in xrange(5):
        myIntegers.append(int(raw_input('Enter an integer: ')))
        
    print(myIntegers)
    writeFile = open('pickledInts.obj', 'w')
    cPickle.dump(myIntegers, writeFile)

def doUnpickle():
    readFile = open('pickledInts.obj', 'r')
    myIntegers = cPickle.load(readFile)
    print(myIntegers)

input = str(raw_input('Pickle new (1) or Unpickle existing (2) ?: '))
options = ({'1': '!doPickle()', '2': '!doUnpickle()'})
sel = options.get(input, '!showError()')
eval(sel.replace('!',''))
