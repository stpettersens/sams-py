"""
Test Yedda.Twitter assembly in IronPython
Please see LEGAL.txt for redistribution information
"""
import sys
import clr
clr.AddReference("System.Xml")
clr.AddReference("Yedda.Twitter")
from System.Xml import *
from System.Diagnostics import Process
from Yedda import Twitter

p = Process()
t = Twitter()

def followers(screenName):
	print(t.GetUserFollowersAsJSON(screenName))

def real_name(IDorScreenName):
	print(t.GetRealName(IDorScreenName))

def screen_name(userID):
	print(t.GetScreenName(userID))

def user_id(screenName):
	print(t.GetUserID(screenName))

def location(IDorScreenName):
	print(t.GetUserLoc(IDorScreenName))

def biog(IDorScreenName):
	print(t.GetUserBiog(IDorScreenName))

def image(IDorScreenName):
	url = t.GetUserImg(IDorScreenName)
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
			print(t.GetScreenName(ids.Item(i).InnerText))
			i += 1

def main():
	print("\nRun this in IronPython interactive mode.")
	print("\nipy")
	print(">>import twitter")
	print(">>twitter.<method>")

if __name__ == "__main__": main()

