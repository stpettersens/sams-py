/*
 * Gauldi platform agnostic build tool

 * Copyright (c) 2010 Sam Saint-Pettersen
 * 
 * Released under the MIT License.
 * 
*/
package gauldi
import scala.io.Source
import java.io.IOException
import java.util.{HashMap => JHashMap}

object GauldiApp {
  val buildFile: String = "C:\\build.json" 
  def main(args: Array[String]): Unit = {
	  // Default behavior is to load project's build file
	  if(args.length == 0) loadBuild(buildFile)
  }
  // Load build file
  def loadBuild(buildFile: String): Unit = {
	  var buildConf: String = ""
	  try {
	 	  for(line <- Source.fromFile(buildFile).getLines()) {
	 	 	  buildConf += line
	 	  }
	 	  // Shrink string, by replacing tabs with spaces;
	 	  // Gaudli build files should be written using tabs
	 	  buildConf = buildConf.replaceAll("\t","")
	  }
	  catch { // Catch I/O & general exceptions
	 	  case ioe: IOException => displayError(ioe)
	 	  case e: Exception => displayError(e)
	  }
	  finally { // Parse configuration via GauldiBuildParser class
	 	  val buildParser = new GauldiBuildParser(buildConf)
	 	  println(buildParser.getRaw()) // DEBUG!

	  }
  }
  def generateNativeFile(): Unit = {
  }
  def generateMakefile(buildFile: String): Unit = {
	  
  }
  def displayError(ex: Exception): Unit = {
	  println(ex)
	  displayUsage()
  }
  def displayUsage(): Unit = {
	  
  }
}