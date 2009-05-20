//
// Nitwit
// Twitter client library for .NET
// Inspired by Yedda.Twitter
// Version 1.0
// Copyright (c) Sam Saint-Pettersen
//
// Released under the MIT License
//
using System;
using System.Collections.Generic;
using System.Text;
using System.Net;
using System.Xml;

namespace Nitwit {

    public class Twitter {
        #region Defines
        // Define Twitter base and API URL format
        protected const string BaseUrl = @"http://twitter.com";
        protected const string ApiUrl = @BaseUrl + "/{1}/{2}.{3}";
       
        // Define API groups and methods
        protected enum ApiGroup : short {  
            // {1} in ApiUrl
            Statuses, Users, Direct_messages, // REST API groups
            Friendships, Friends, Followers, Favorites,
            Accounts, Notifications, Blocks, Help,
            Search, Trends  // Search API groups
        }
        protected enum ApiMethod : short {
            // {2} in ApiUrl
            Public_timeline, Friends_timeline, // Timeline methods
            User_timeline, Show, Friends, Followers, // User methods
            Sent, New, Create, Exists, Destroy, IDs, // "Overloaded" methods
            Follow, Leave, // Notification methods
            Blocking, // Blocks method(s)
            Test // Help method
        }

        // Define returned data formats
        public enum DataFormat : byte {
            Atom, RSS, XML, JSON // {3} in ApiUrl
        }

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

        public string testMethod() {
            DataFormat format = DataFormat.Atom;
            return getFormatStr(format);
        }
    }
}
