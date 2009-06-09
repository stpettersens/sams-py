// <JETPACK>
// @title: 360ify 
// @description: Xbox 360 achievements notifier
// @author: Sam Saint-Pettersen
// @url: http://code.google.com/p/sams-py
// @license: MIT License
// Special thanks to Duncan Mackenzie (@duncanma) 
// for his Xbox gamertag REST API which this script uses.
// http://bit.ly/xboxgtapi
// http://duncanmackenzie.net
// </JETPACK>
var xboxLive = 'http://live.xbox.com';
var xboxIcon = 'http://img8.imageshack.us/img8/7338/360ifyr.png';
var xboxGTApi = 'http://duncanmackenzie.net/services/GetXboxInfo.aspx?Gamertag=';
var gamerTag = 'earlsKarma'; // Temporary, gamer tag will be able to be set
var achievements = null;
function openProfile() {
	
}
function lastAchievement() {
    jetpack.notifications.show(
    {title: "Last Achievement ", body: 'Something cool!', icon: xboxIcon});
}
function newAchievement() {
	
}
jetpack.statusBar.append({
    html: '<img src="' + xboxIcon + '">',
    width: 16,
    onReady: function(doc) {
    $(doc).find("img").click(function() {
        lastAchievement();
    });
}});
