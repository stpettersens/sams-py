"""
Queue proof-of-concept
"""
import Queue

queue = Queue.Queue()
queue.put('Hello')
queue.put('Goodbye')
queue.put('Hello again')

print(queue.get()) # Get 1st element
print(queue.get()) # Get 2nd element
print(queue.get()) # Get 3rd element
