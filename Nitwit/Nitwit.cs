//
// Nitwit
// Twitter client library for .NET
// Inspired and influenced by Yedda.Twitter
// Version 1.0
// Copyright (c) Sam Saint-Pettersen
//
// Released under the MIT License
//
using System;
using System.Collections.Generic;
using System.Text;
using System.IO;
using System.Net;
using System.Xml;

namespace SamsPy {

    public class NitWit {

        #region LibraryDefines

        // Define Twitter API URL format
        private const string ApiUrl = @"http://twitter.com/{0}/{1}.{2}";
       
        // Define API groups and methods
        private enum ApiGroup : byte {  
            // {0} in ApiUrl
            Statuses, Users, Direct_messages, // REST API groups
            Friendships, Friends, Followers, Favorites,
            Accounts, Notifications, Blocks, Help,
            Search, Trends  // Search API groups
        }

        private enum ApiMethod : byte {
            // {1} in ApiUrl
            Public_timeline, Friends_timeline, // Timeline methods
            User_timeline, Show, Friends, Followers, // User methods
            Sent, New, Create, Exists, Destroy, IDs, // Common methods
            Follow, Leave, // Notification methods
            Blocking, // Blocks method(s)
            Test // Help method
        }

        // Define returned data formats
        public enum DataFormat : byte { JSON, XML, RSS, Atom } // {2} in ApiUrl

        // Special appendings
        private enum Append : byte { User_a, User_b, Follow } // After {2} in ApiUrl

        // Return an ApiGroup as a lowercase string
        private string getGroupStr(ApiGroup group) {
            return group.ToString().ToLower();
        }

        // Return an ApiMethod as a lowercase string
        private string getMethodStr(ApiMethod method) {
            return method.ToString().ToLower();
        }

        // Return a DataFormat as a lowercase string
        private string getFormatStr(DataFormat format) {
            return format.ToString().ToLower();
        }

        // Return an Append as a lowercase string in correct 
        // appending context
        private string getAppendStr(Append app) {
            string sym = null; 
            if(app == Append.User_a) sym = @"?"; else sym = @"&";
            return string.Format("{0}{1}{2}", sym,
            app.ToString().ToLower(), @"=");
        }

        // Alternative method for returning Append as a string
        private string getAppendStr(ApiMethod app) {
            return string.Format(@"?{0}{1}", app.ToString().ToLower(), @"=");
        }


        #endregion

        #region ClientDefines
        #endregion

        #region Library_methods

        /// <summary>
        /// Execute HTTP GET method w/ or w/o authentication
        /// </summary>
        /// <param name="url">URL for response</param>
        /// <param name="username">Authenticating user's username (optional)</param>
        /// <param name="password">Authenticating user's password (optional)</param>
        private string executeHttpGet(string url, string username, string password) {
            WebClient client = new WebClient();
            if(!string.IsNullOrEmpty(username) && !string.IsNullOrEmpty(password)) {
                client.Credentials = new NetworkCredential(username, password);
            }
            try
            {
                Stream stream = client.OpenRead(url);
                StreamReader reader = new StreamReader(stream);
                return reader.ReadToEnd();
            }
            catch (WebException ex)
            {
                if (ex.Response is HttpWebResponse)
                {
                    // Return null on HTTP 404 - Not Found
                    if ((ex.Response as HttpWebResponse).StatusCode == HttpStatusCode.NotFound)
                    {
                        return null;
                    }
                }
                throw ex;
            }
        }

        /// <summary>
        /// Execute HTTP POST method w/ user authentication
        /// </summary>
        /// <param name="url">URL for request</param>
        /// <param name="username">Authenticating user's username</param>
        /// <param name="password">Authenticating user's password</param>
        /// <returns>Request response or null</returns>
        private string executeHttpPost(string url, string username, string password) {
            // Do not expect HTTP 100, prevents HTTP 417 problem
            ServicePointManager.Expect100Continue = false;
            WebRequest request = WebRequest.Create(url);
            request.Credentials = new NetworkCredential(username, password);
            request.ContentType = "application/x-www-form-urlencoded";
            request.Method = "POST";

            // ...
            
            string data = "";
            byte[] bytes = Encoding.UTF8.GetBytes(data); // Use UTF8 encoding
            request.ContentLength = bytes.Length;
            Stream requestStream = request.GetRequestStream();
            requestStream.Write(bytes, 0, bytes.Length);
            WebResponse response = request.GetResponse();
            using(StreamReader reader = 
            new StreamReader(response.GetResponseStream())) {
                        return reader.ReadToEnd();
            }
        }

        #endregion

        #region REST_API_methods

        #region Help_methods

        /// <summary>
        /// Twitter API Doc: Returns the string "ok" in the requested format 
        /// with a 200 OK HTTP status code.
        /// NOT AUTHENTICATED, NOT API LIMITED
        /// "http://apiwiki.twitter.com/Twitter-REST-API-Method:-help test"
        /// </summary>
        /// <param name="format">Data format to return response in</param>
        /// <returns>Reponse in specified data type</returns>
        public string testMethod(DataFormat format) {
            if(format == DataFormat.RSS || format == DataFormat.Atom) {
                throw new ArgumentException("testMethod supports only JSON or XML response.");
            }
            string url = string.Format(ApiUrl, getGroupStr(ApiGroup.Help),
            getMethodStr(ApiMethod.Test), getFormatStr(format));
            return executeHttpGet(url, null, null);
        }

        // Convenience methods to return response in a specific data format
        public string testMethodInJSON() {
            return testMethod(DataFormat.JSON);
        }

        public string testMethodInXML() {
            return testMethod(DataFormat.XML);
        }

        #endregion

        #region Public_Timeline

        /// <summary>
        /// Twitter API Doc: Returns the 20 most recent statuses from 
        /// non-protected users who have set a custom user icon.
        /// </summary>
        /// <param name="format">Data format to return reponse in</param>
        /// <returns>Specified data format</returns>
        public string getPublicTimeline(DataFormat format) {
            string url = string.Format(ApiUrl, getGroupStr(ApiGroup.Statuses), 
            getMethodStr(ApiMethod.Public_timeline), getFormatStr(format));
            return executeHttpGet(url, null, null);
        }

        // Convenience methods for getting public timeline in a specific format
        public string getPublicTimeLineInJSON() {
            return getPublicTimeline(DataFormat.JSON);
        }

        public XmlDocument getPublicTimeLineInXML(DataFormat xmlFormat) {
            if (xmlFormat == DataFormat.JSON) {
                throw new ArgumentException
                ("getPublicTimeLineInXML supports only XML, RSS or Atom", "format");
            }
            string output = getPublicTimeline(xmlFormat);
            if (!string.IsNullOrEmpty(output)) {
                XmlDocument timeline = new XmlDocument();
                timeline.LoadXml(output);

                return timeline;
            }
            return null;
        }

        public XmlDocument getPublicTimeLineInXML() {
            return getPublicTimeLineInXML(DataFormat.XML);
        }

        public XmlDocument getPublicTimeLineInRSS() {
            return getPublicTimeLineInXML(DataFormat.RSS);
        }

        public XmlDocument getPublicTimeLineInAtom() {
            return getPublicTimeLineInXML(DataFormat.Atom);
        }

        #endregion

        #region User_Timeline
        #endregion

        #region Status_methods

        /// <summary>
        /// Twitter API Doc: Returns a single status, specified by
        /// the id parameter below. The status's author will be returned inline.
        /// </summary>
        /// <param name="statusID">Status ID for Tweet</param>
        /// <returns>Tweet and author inline.</returns>
        public string getStatus(string statusID, DataFormat format) {
            string url = String.Format(ApiUrl, getGroupStr(ApiGroup.Statuses),
            getMethodStr(ApiMethod.Show), getFormatStr(format));
            return executeHttpGet(url, null, null);
        }

        #endregion

        #region User_methods
        #endregion

        #region Direct_message_methods
        #endregion

        #region Friendship_methods

        /// <summary>
        /// Twitter API Doc: Tests for the existance of friendship between two users. 
        /// Will return true if user_a follows user_b, otherwise 
        /// will return false.
        /// Response types: JSON, XML (and raw Boolean via JSON in Nitwit)
        /// IS API LIMITED, IS AUTHENTICATED
        /// "http://apiwiki.twitter.com/Twitter-REST-API-Method:-friendships-exists"
        /// </summary>
        /// <param name="username">Authenticating user's username</param>
        /// <param name="password">Authenticating user's password</param>
        /// <param name="userA">First user in comparison</param>
        /// <param name="userB">Second user in comparison</param>
        /// <param name="format">Data format to return response in</param>
        /// <returns>Returns reponse in specified data format</returns>
        public string areFriends(string username, string password, string userA,
        string userB, DataFormat format) {
            if(format == DataFormat.RSS || format == DataFormat.Atom) {
                throw new ArgumentException("areFriends supports only JSON or XML response.");
            }
            string url = string.Format(ApiUrl, getGroupStr(ApiGroup.Friendships),
            getMethodStr(ApiMethod.Exists), getFormatStr(format) +
            getAppendStr(Append.User_a) + userA + getAppendStr(Append.User_b) + userB);
            return executeHttpGet(url, username, password);
        }

        public string areFriendsInJSON(string username, string password, string userA,
        string userB) {
            return areFriends(username, password, userA, userB, DataFormat.JSON);
        }

        public XmlDocument areFriendsInXML(string username, string password, string userA,
        string userB) {
            string output = areFriends(username, password, userA, userB, DataFormat.XML);
            if (!string.IsNullOrEmpty(output))
            {
                XmlDocument response = new XmlDocument();
                response.LoadXml(output);
                return response;
            }
            return null;
        }

        public bool areFriendsInBool(string username, string password, string userA,
        string userB) {
            string response = areFriendsInJSON(username, password, userA, userB);
            if (response == "true") return true;
            else if (response == "false") return false;
            else return false; // Assume false on bad response
        }

        /// <summary>
        /// Twitter API Doc: Allows the authenticating user to follow the user 
        /// specified in the ID parameter.  
        /// Returns the befriended user in the requested format when successful.
        /// Returns a string describing the failure condition when unsuccessful.
        /// Response types: JSON, XML 
        /// NOT API LIMITED, IS AUTHENTICATED
        /// "http://apiwiki.twitter.com/Twitter-REST-API-Method:-friendships create"
        /// </summary>
        /// <param name="username">Authenticating user's username</param>
        /// <param name="password">Authenticating user's password</param>
        /// <param name="IDorScreenName">ID or screen name of user to follow</param>
        /// <param name="notifs">Add followed user's notifications to profile</param>
        /// <param name="format">Data format to return response in</param>
        /// <returns>Returns reponse is specified data format</returns>
        public string addFriend(string username, string password, string IDorScreenName,
        bool notifs, DataFormat format) {
            if(format == DataFormat.RSS || format == DataFormat.Atom) {
                throw new ArgumentException("followUser only accepts JSON or XML response.");
            }
            string url = string.Format(ApiUrl, getGroupStr(ApiGroup.Friendships), 
            getMethodStr(ApiMethod.Create) + "/" + IDorScreenName, getFormatStr(format));
            if(notifs) {
                url += string.Format(getAppendStr(ApiMethod.Follow) + notifs.ToString().ToLower());
            }
            return executeHttpPost(url, username, password);
        }

        public string addFriendInJSON(string username, string password, string IDorScreenName,
        bool notifs) {
            return addFriend(username, password, IDorScreenName, notifs, DataFormat.JSON);
        }

        public XmlDocument addFriendInXML(string username, string password, string IDorScreenName,
        bool notifs) {
            string output = addFriend(username, password, IDorScreenName, notifs, DataFormat.XML);
            if (!string.IsNullOrEmpty(output))
            {
                XmlDocument response = new XmlDocument();
                response.LoadXml(output);
                return response;
            }
            return null;
        }

        /// <summary>
        /// Twitter API Doc: Allows the authenticating users to unfollow the user specified in 
        /// the ID parameter. Returns the unfollowed user in the requested format when successful. 
        /// Returns a string describing the failure condition when unsuccessful.
        /// Response types: JSON, XML 
        /// NOT API LIMITED, IS AUTHENTICATED
        /// "http://apiwiki.twitter.com/Twitter-REST-API-Method:-friendships destroy"
        /// </summary>
        /// <param name="username">Authenticating user's username</param>
        /// <param name="password">Authenticating user's password</param>
        /// <param name="IDorScreenName">ID or screen name of user to unfollow</param>
        /// <param name="format">Data format to return reponse in</param>
        /// <returns>Returns response in specified data format</returns>
        public string removeFriend(string username, string password, string IDorScreenName,
        DataFormat format) {
            if (format == DataFormat.RSS || format == DataFormat.Atom) {
                throw new ArgumentException("removeFriend only accepts JSON or XML response.");
            }
            string url = string.Format(ApiUrl, getGroupStr(ApiGroup.Friendships),
            getMethodStr(ApiMethod.Destroy) + "/" + IDorScreenName, getFormatStr(format));
            Console.WriteLine("Debug::" + url);
            return executeHttpPost(url, username, password);
        }

        public string removeFriendInJSON(string username, string password, string IDorScreenName) {
            return removeFriend(username, password, IDorScreenName, DataFormat.JSON);
        }

        public XmlDocument removeFriendInXML(string username, string password, string IDorScreenName) {
            string output = removeFriend(username, password, IDorScreenName, DataFormat.XML);
            if (!string.IsNullOrEmpty(output)) {
                XmlDocument response = new XmlDocument();
                response.LoadXml(output);
                return response;
            }
            return null;
        }
               
        #endregion

        #endregion

    }
}
