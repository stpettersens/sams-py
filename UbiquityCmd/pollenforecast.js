/* 
   Get the UK pollen forecast for your postcode from GMTV
*/
CmdUtils.CreateCommand({
  names: ["pollen", "pollen count", "check pollen", "forecast pollen"],
  icon: "http://img17.imageshack.us/img17/4381/flowericon.gif",
  homepage: "http://code.google.com/p/sams-py",
  author: {name: "Sam Saint-Pettersen", email: "s.stpettersen@gmail.com"},
  license: "MIT",
  description: "Get the UK pollen forecast for postcode from GMTV",
  arguments: [{role: 'object', nountype: noun_arb_text, label: 'post code'}],
  preview: function(pblock, args) {
  	var data = {};
	data.query = args.object.text;
  	var url = "http://www.gm.tv/index.cfm?article=2932&symbolPrefix=p" 
	+ "&postcode=" + data.query + "&articleID=2932&showWorldRegion=3&showTab=1";
	$.get(url, function(page) {
		var formatted = $(page).find(".weatherText").text()
		.replace(/Weather UV Index Pollen Count-/, "");
		formatted = formatted.replace(/United Kingdom - Europe/, "")
		formatted = formatted.replace(/\d+\s{1}\w{3}/g, ""); // Strip out dates, just keep days
		formatted = formatted.replace(/HIGH/g, 
		"<span style='font-weight: bold; color: #ff0000;'>H</span>");
		formatted = formatted.replace(/MEDIUM/g,
		"<span style='font-weight: bold; color: #ff6600;'>M</span>");
		formatted = formatted.replace(/Pollen forecast is not available./,
		"<span style='font-style: italic; color: #999999'>No forecast</span>");
		data.forecast = formatted;
    	pblock.innerHTML = CmdUtils.renderTemplate(
		"The pollen count forecast for UK <b>${query}</b> from GMTV" +
		"<p style='font-size: 16px'>${forecast}</p>", data);
	});
  },
  execute: function(object, args){
  	var url = "http://www.gm.tv/index.cfm?article=2932&symbolPrefix=p" 
	+ "&articleID=2932&showWorldRegion=3&showTab=1";
  	Utils.openUrlInBrowser(url);
  }
});
