// <JETPACK>
// @title: 360ify 
// @description: Xbox 360 achievements notifier
// @author: Sam Saint-Pettersen
// @url: http://code.google.com/p/sams-py
// @license: MIT License
// Special thanks to Duncan Mackenzie (@duncanma) 
// for his Xbox gamertag REST API which this script uses.
// This work is in no way affliated with or otherwise endorsed 
// by Microsoft Corporation.
// http://bit.ly/xboxgtapi
// http://duncanmackenzie.net
// </JETPACK>
var title = " - 360ify";
var xboxLive = 'http://live.xbox.com';
var xboxIcon = 'http://img8.imageshack.us/img8/7338/360ifyr.png';
var xboxGTApi = 'http://duncanmackenzie.net/services/GetXboxInfo.aspx';
var gamerTag = 'earlsKarma'; // Temporary, gamer tag will be able to be set
function showProfile() {
    // Cannot make cross domain requests with current Jetpack like you can with Greasemonkey
    // work around is to try to use Greasemonkey for getting the feeds (?)
}
jetpack.statusBar.append({
    html: '<img src="' + xboxIcon + '">',
    width: 16,
    onReady: function(doc) {
    $(doc).find("img").click(function() {
        showProfile();
    });
}});
