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

namespace Nitwit {

    public class Twitter {
        #region LibraryDefines
        // Define Twitter base and API URL format
        protected const string BaseUrl = @"http://twitter.com";
        protected const string ApiUrl = @BaseUrl + "/{0}/{1}.{2}";
       
        // Define API groups and methods
        protected enum ApiGroup : byte {  
            // {0} in ApiUrl
            Statuses, Users, Direct_messages, // REST API groups
            Friendships, Friends, Followers, Favorites,
            Accounts, Notifications, Blocks, Help,
            Search, Trends  // Search API groups
        }
        protected enum ApiMethod : byte {
            // {1} in ApiUrl
            Public_timeline, Friends_timeline, // Timeline methods
            User_timeline, Show, Friends, Followers, // User methods
            Sent, New, Create, Exists, Destroy, IDs, // "Overloaded" methods
            Follow, Leave, // Notification methods
            Blocking, // Blocks method(s)
            Test // Help method
        }

        // Define returned data formats
        public enum DataFormat : byte { Atom, RSS, XML, JSON } // {2} in ApiUrl

        // Return an ApiGroup as a lowercase string
        protected string getGroupStr(ApiGroup group) {
            return group.ToString().ToLower();
        }

        // Return an ApiMethod as a lowercase string
        protected string getMethodStr(ApiMethod method) {
            return method.ToString().ToLower();
        }

        // Return a DataFormat as a lowercase string
        protected string getFormatStr(DataFormat format) {
            return format.ToString().ToLower();
        }
        #endregion

        #region ClientDefines
        #endregion

        #region LibraryMethods
        /// <summary>
        /// Execute HTTP GET method w/o authentication
        /// </summary>
        /// <param name="url">URL for operation</param>
        /// <returns>Request response or null</returns>
        protected string executeHttpGet(string url) {
            WebClient client = new WebClient();
            try {
                using (Stream stream = client.OpenRead(url)) {
                    using(StreamReader reader = new StreamReader(stream)) {
                        return reader.ReadToEnd();
                    }
                }
            }
            catch(WebException ex) {
                if (ex.Response is HttpWebResponse) {
                    // Return null on HTTP 404 - Not Found
                    if ((ex.Response as HttpWebResponse).StatusCode == HttpStatusCode.NotFound) {
                        return null;
                    }
                }
                throw ex;
            }

        }
        /// <summary>
        /// Execute HTTP POST method w/ user authentication
        /// </summary>
        /// <param name="url">URL for operation</param>
        /// <param name="username">Authenticating user's username</param>
        /// <param name="password">Authenticating user's password</param>
        /// <param name="data">Data to post</param>
        /// <returns>Request response or null</returns>
        protected string executeHttpPost(string url, string username, string password, string data) {
            // Do not expect HTTP 100, prevents HTTP 417 problem
            ServicePointManager.Expect100Continue = false;
            WebRequest request = WebRequest.Create(url);
            request.Credentials = new NetworkCredential(username, password);
            request.ContentType = "application/x-www-form-urlencoded";
            request.Method = "POST";

            // ...

            byte[] bytes = Encoding.UTF8.GetBytes(data); // Use UTF8 encoding
            request.ContentLength = bytes.Length;
            using(Stream requestStream = request.GetRequestStream()) {
                requestStream.Write(bytes, 0, bytes.Length);
                using(WebResponse response = request.GetResponse()) {
                    using(StreamReader reader = new StreamReader(response.GetResponseStream())) {
                        return reader.ReadToEnd();
                    }
                }
            }
        }
        #endregion

        #region REST_API_methods

        #region Public_Timeline
        /// <summary>
        /// Twitter API: Returns the 20 most recent statuses from non-protected users
        /// who have set a custom user icon.
        /// </summary>
        /// <param name="format">Data format to return reponse in</param>
        /// <returns>Specified data format</returns>
        public string getPublicTimeline(DataFormat format) {
            string url = string.Format(ApiUrl, getGroupStr(ApiGroup.Statuses), 
            getMethodStr(ApiMethod.Public_timeline), getFormatStr(format));
            return executeHttpGet(url);
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
            string url = String.Format
            (ApiUrl, getGroupStr(ApiGroup.Statuses), getMethodStr(ApiMethod.Show),
            getFormatStr(format));
            return executeHttpGet(url);
        }

        #endregion

        #region User_methods
        #endregion

        #region Direct_message_methods
        #endregion

        #region Friendship_methods

        /// <summary>
        /// Twitter API Doc: Allows the authenticating users to follow the user 
        /// specified in the ID parameter.  
        /// Returns the befriended user in the requested format when successful.
        /// Returns a string describing the failure condition when unsuccessful.
        /// </summary>
        /// <param name="username">Authenticating user's username</param>
        /// <param name="password">Authenticating user's password</param>
        /// <param name="IDorScreenName"></param>
        /// <param name="format">Data format to return response in</param>
        /// <returns>Returns reponse is specified data format</returns>
        public string followUser(string username, string password, string IDorScreenName,
        DataFormat format) {
            if(format == DataFormat.Atom || format == DataFormat.RSS) {
                throw new ArgumentException("followUser only accepts JSON or XML response.");
            }
            string url = String.Format(
            ApiUrl, getGroupStr(ApiGroup.Friendships), getMethodStr(ApiMethod.Create) 
            + "/" + IDorScreenName, getFormatStr(format));
            return executeHttpPost(url, username, password, "");
        }

        // Convenience methods for getting response in a specific format
        public string followUserInJSON(string username, string password, string IDorScreenName) {
            return followUser(username, password, IDorScreenName, DataFormat.JSON);
        }

        public XmlDocument followUserInXML(string username, string password, string IDorScreenName)
        {
            string output = followUser(username, password, IDorScreenName, DataFormat.XML);
            if (!string.IsNullOrEmpty(output))
            {
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
