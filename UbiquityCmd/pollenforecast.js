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
  	var baseUrl = "http://www.gm.tv/index.cfm?article=2932&symbolPrefix=p";
	if (data.query.search(/[a-z]{1,2}\d{1,2}\s?\d{0,1}[a-z]{0,2}/ig) != -1) {
		var url = baseUrl + "&postcode=" + data.query + "&articleID=2932&showWorldRegion=3&showTab=1";
		$.get(url, function(page){
			var formatted = $(page).find(".weatherText").text()
			.replace(/Weather UV Index Pollen Count-/, ""); // Strip out redundant text
			formatted = formatted.replace(/United Kingdom - Europe/, "") 
			formatted = formatted.replace(/\d+\s{1}\w{3}/g, ""); // Strip out dates, just keep days
			formatted = formatted.replace(/not be/, "could not be"); // Correct grammar for errors
			formatted = formatted.replace(/Select[\w\s\n\-\.]*/gm, "") // Strip out any verbose errors
			formatted = formatted.replace(/HIGH/g,
			 "<span style='font-size: 20px; font-weight: bold; color: #ff0000;'>H</span>");
			formatted = formatted.replace(/MEDIUM/g, 
			"<span style='font-size: 20px; font-weight: bold; color: #ff6600;'>M</span>");
			formatted = formatted.replace(/Pollen forecast is not available./, 
			"<span style='font-style: italic; color: #999999'>No forecast</span>");
			data.forecast = formatted;
			pblock.innerHTML = CmdUtils.renderTemplate(
			"The pollen count forecast for <span style='font-weight: bold'>" +
			"${query}</span> from GMTV" +
			"<p style='font-size: 16px'>${forecast}</p>", data);
		});
	}
	else pblock.innerHTML = CmdUtils.renderTemplate("Hit <span style='font-weight: bold'>" 
	+ "enter</span> for the pollen count forecast for UK from GMTV");
  },
  execute: function(object, args){
  	var url = "http://www.gm.tv/index.cfm?article=2932&symbolPrefix=p" 
	+ "&articleID=2932&showWorldRegion=3&showTab=1";
  	Utils.openUrlInBrowser(url);
  }
});
