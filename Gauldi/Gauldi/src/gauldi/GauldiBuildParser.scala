/*
 * Gauldi platform agnostic build tool
 * Copyright (c) 2010 Sam Saint-Pettersen
 * 
 * Released under the MIT License.
 * 
*/
package gauldi
import org.json.simple.{JSONValue,JSONObject,JSONArray}

class GauldiBuildParser(buildConf: String) {
	
	// Return raw build configuration in string,
	// for debugging pu\rposes only
	def getBuildString(): String = {
		buildConf
	}
	def getPreamble(): JSONObject = {
		parseBuildJSON()
		// Put into new JSONObject...
	}
	def getBuildSteps(): JSONArray = {
		//parseBuildJSON()
		// Sort into JSONArray...
		new JSONArray()
	}
	def getInstallSteps(): JSONArray = {
		new JSONArray()
	}
	def getCleanSteps(): JSONArray = {
		parseBuildJSON()
		// Sort into JSONArray...
		new JSONArray()
	}
	private def parseBuildJSON(): JSONObject = { 
		val parsedJson: Object = JSONValue.parse(buildConf)
		val jsonObj: JSONObject = parsedJson.asInstanceOf[JSONObject]
		jsonObj
	}
}