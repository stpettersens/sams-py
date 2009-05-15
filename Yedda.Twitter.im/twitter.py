"""
Test Yedda.Twitter assembly in IronPython
Please see LEGAL.txt for redistribution information
"""
import clr
clr.AddReference("System.Xml")
clr.AddReference("Yedda.Twitter")
from System.Xml import *
from System.Diagnostics import Process
from Yedda import Twitter

p = Process()
t = Twitter()

def followers(IDorScreenName):
	print(t.GetUserFollowersAsJSON(IDorScreenName))

def user_details(IDorScreenName):
	global userDetails
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
	url = t.GetUserImg(userDetails)
	print(url)
	p.StartInfo.FileName = url
	p.Start()

def show(userName, password):
	print(t.ShowAsJSON(userName, password, userName))

def each_follower(screenName):
	followers = t.GetUserFollowersAsXML(screenName)
	ids = followers.GetElementsByTagName("id")
	i = 0
	while i < ids.Count:
		print(ids.Item(i).InnerText)
		i += 1

def main():
	print("\nRun this in IronPython interactive mode.")
	print("\nipy")
	print(">>>import twitter")
	print(">>>twitter.<method>")

if __name__ == "__main__": main()
