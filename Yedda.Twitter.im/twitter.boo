"""
Test Yedda.Twitter assembly in Boo
Please see LEGAL.txt for redistribution information
"""
import System.Xml
import System.Diagnostics
import Yedda.Twitter

p as Process = Process()
t as Yedda.Twitter = Yedda.Twitter()
userDetails as XmlDocument = null

def followers(IDorScreenName as string):
	print(t.GetUserFollowersAsJSON(IDorScreenName))

def user_details(IDorScreenName as string):
	userDetails = t.GetUserDetailsAsXML(IDorScreenName)

def real_name():
	print(t.GetRealName(userDetails))

def screen_name():
	print(t.GetScreenName(userDetails))

def user_id():
	print(t.GetUserID(userDetails))

def location():
	print(t.GetUserLoc(userDetails))

def time_zone():
	print(t.GetUserTimeZone(userDetails))

def biog():
	print(t.GetUserBiog(userDetails))

def image():
	url as string = t.GetUserImg(userDetails)
	print(url)
	p.StartInfo.FileName = url
	p.Start()

def show(userName as string, password as string):
	print(t.ShowAsJSON(userName, password, userName))

def each_follower(IDorScreenName as string):
	followers as XmlDocument = t.GetUserFollowersAsXML(IDorScreenName)
	ids as XmlNodeList = followers.GetElementsByTagName("id")
	print("${ids.Count} followers:")
	i as int = 0
	while i < ids.Count:
		print(ids.Item(i).InnerText)
		i += 1

def each_friend(IDorScreenName as string):
	friends as XmlDocument = t.GetUserFriendsAsXML(IDorScreenName)
	ids as XmlNodeList = friends.GetElementsByTagName("id")
	print("${ids.Count} friends:")
	i as int = 0
	while i < ids.Count:
		print(ids.Item(i).InnerText)
		i += 1

def update(username as string, password as string, status as string):
	t.UpdateNow(username, password, status)
	print("Tweeted: ${status}!")

def main():
	print("\nRun this in Boo interactive shell.")
	print("\nbooish twitter.boo")
	print(">>><method>")

main()
