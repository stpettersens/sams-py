"""
Test Nitwit Twitter client library in booish
"""
namespace TwitterTest
import Nitwit.Twitter
import System.IO

t as Nitwit.Twitter = Nitwit.Twitter()
u as string = "testuser100"
tr as TextReader = StreamReader("pwd.txt")
p as string = tr.ReadLine()

print "Test Nitwit Twitter client library"
print "Use 't' for Nitwit object"
print "Use 'u' for username"
print "Use 'p' for password (pwd.txt, not in SVN)"
print "Ready for testing. :)"

def add_friend(user as string):
  if t.areFriendsInBool(u, p, u, user):
    print("${u} and ${user} are already friends.")
  else:
    t.addFriendInJSON(u, p, user, true)
    print("${u} is now following ${user}!")
    
def remove_friend(user as string):
  if t.areFriendsInBool(u, p, u, user) == false:
    print("${u} is not following ${user}!")
  else:
    t.removeFriendInJSON(u, p, user);
    print("${u} is no longer following ${user}.")
