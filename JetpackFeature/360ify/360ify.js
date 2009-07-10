// 
// @title: 360ify 
// @description: Xbox 360 achievements notifier for Jetpack
// @author: Sam Saint-Pettersen
// @url: http://code.google.com/p/sams-py
// @license: MIT License
// Special thanks to Duncan Mackenzie (http://duncanmackenzie.net) 
// for his Xbox gamertag REST API which this script uses.
// This work is in no way affliated with or otherwise endorsed 
// by Microsoft Corporation.
// http://bit.ly/xboxgtapi
//
var xboxLive = 'http://live.xbox.com/member/';
var xboxIcon = 'http://img8.imageshack.us/img8/7338/360ifyr.png';
var xboxGTApi = 'http://duncanmackenzie.net/services/GetXboxInfo.aspx?GamerTag=';
var gamerTag = 'uberSamji'; // %GAMER% Gamer tag will be set at install time
var apiUrl = xboxGTApi + gamerTag;
var profUrl = xboxLive + gamerTag;
var finalG = null;
function getProfile(){
	$.get(apiUrl, function(xbp) {
		var caption = gamerTag + ' on Xbox Live';
        var gamerIcon = $(xbp).find('TileUrl').text();
        var gameScore = $(xbp).find('GamerScore:first').text();
        var gamerRepu = $(xbp).find('Reputation').text();
        var lastGameT = $(xbp).find('Game:first').find('Name').text();
        var lastGameG = $(xbp).find('XboxUserGameInfo:first').find('GamerScore').text();;
        var lastGameA = $(xbp).find('XboxUserGameInfo:first').find('Achievements').text();
        var lastGameTG = $(xbp).find('TotalGamerScore:first').text();
        var lastGameTA = $(xbp).find('TotalAchievements:first').text();
		
        // When no values found in XML, use these defaults
        if(lastGameT == '') lastGameT = 'No games played.';
        if(lastGameG == '') lastGameG = 0;
        if(lastGameA == '') lastGameA = 0;
        if(lastGameTG == '') lastGameTG = 0;
        if(lastGameTA == '') lastGameTA = 0;
		
        // Convert rating percentage to stars out of 5
        gamerRepu = Math.round(parseFloat(gamerRepu / 20));
        // Parse gamer score as integer, so we can tell if its changed since last time
        finalG = parseInt(gameScore);
        var msg = 'G: ' + gameScore + '  Rep: ' + gamerRepu + '/5  ' + lastGameT +
        '  (G: ' + lastGameG + '/' + lastGameTG + '  Ach: ' + lastGameA + '/' +  lastGameTA + ')';
        jetpack.notifications.show({title: caption, body: msg, icon: gamerIcon});
        if(jetpack.tabs.focused.url.match(/xbox/) == null) {
            var profTab = jetpack.tabs.open(profUrl);
			profTab.focus();
        }
    });
}
// Append Xbox icon to status bar
jetpack.statusBar.append({
    html: '<img src="' + xboxIcon + '"\/>',
    width: 16,
    onReady: function(doc){
        $(doc).find("img").click(function(){
            getProfile();
        });
    }
})
