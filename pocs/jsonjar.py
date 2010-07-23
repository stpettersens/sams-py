"""
Demonstrate JSON module
with an application to serialize and deserialize an array (list) of integers.
Similar to Pickle, but I can have neater structures
"""
import json
from encodings import hex_codec # Explicit import for JSON with Freeze

def showError():
    print('You must enter either 1 or 2!')

def doSerialize():
    myIntegers = []
    for i in xrange(5):
        myIntegers.append(int(raw_input('Enter an integer: ')))
        
    print(myIntegers)
    writeFile = open('jsonInts.json', 'w')
    json.dump(myIntegers, writeFile)

def doDeserialize():
    readFile = open('jsonInts.json', 'r')
    myIntegers = json.load(readFile)
    print(myIntegers)

input = str(raw_input('Serialize new (1) or Deserialize existing (2) ?: '))
options = ({'1': '!doSerialize()', '2': '!doDeserialize()'})
sel = options.get(input, '!showError()')
eval(sel.replace('!',''))
