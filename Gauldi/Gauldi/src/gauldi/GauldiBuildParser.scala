/*
 * Gauldi platform agnostic build tool
 * Copyright (c) 2010 Sam Saint-Pettersen
 * 
 * Released under the MIT License.
 * 
*/
package gauldi
import java.util.{HashMap => JHashMap}
import org.json.simple.JSONValue

class GauldiBuildParser(buildConf: String) {
	
	// Return raw configuration, for debugging purposes only
	def getRaw(): String = {
		buildConf
	}
	def getPreamble(): JHashMap[String,String] = {
		parseBuildJSON(0)
	}
	def getBuildSteps(): JHashMap[String,String] = {
		parseBuildJSON(1)
	}
	def getCleanSteps(): JHashMap[String,String] = {
		parseBuildJSON(2)
	}
	private def parseBuildJSON(section: Int): JHashMap[String,String] = {
		val keyPairs = new JHashMap[String,String]
		keyPairs
	}
}