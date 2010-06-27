# Use a Python dictionary
# as a substitute for other languages' switch statement

def doSomething():
    print('I just did something')
    
var = 'funct'
a = 'localhost'
values = ({
		'host': a,
		'funct': '!doSomething()'
		})
x = values.get(var)
if x.startswith('!'): eval(x.replace('!', ''))
else: print(x)
