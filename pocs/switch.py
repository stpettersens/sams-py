# Use a Python dictionary
# as a substitute for other languages' switch statement
#
# X is equivalent to this switch in C++:
#
#		string var = 'apple';
# 		switch(var) {
#			case 'pineapple':
#				orderPineapple();
#				break;
#			case 'apple':
#				orderApple();
#				break;
#			case 'strawberry':
#				orderStrawberry();
#				break;
#			default:
#				orderOther();
#		}
#
def orderPineapple():
	print 'You ordered pineapple.'

def orderApple():
	print 'You ordered apple.'

def orderStrawberry():
	print 'You ordered strawberry.'
	
def orderOther():
	print 'You ordered something else.'
	
# X:
var = 'apple'
values = ({
		'pineapple': 'orderPineapple()',
		'apple': 'orderApple()',
		'strawberry': 'orderStrawberry()'
		})
eval(values.get(var, 'orderOther()'))
