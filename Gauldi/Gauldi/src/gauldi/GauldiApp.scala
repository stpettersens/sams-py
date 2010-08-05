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
import org.json.simple.{JSONObject,JSONArray}

object GauldiApp {
  // Default build file
  val buildFile: String = "build.json"
  def main(args: Array[String]): Unit = {
	  // Default behavior is to load project's build file
	  if(args.length == 0) doBuild(buildFile)
	  // Handle command line arguments
	  else if(args.length == 2) {
	 	  args(0) match {
	 	 	  case "-f" => doBuild(args(1))
	 	  }
	  }
	  else if(args.length == 1) {
	 	  args(0) match {
	 	 	  case "-i" => displayUsage()
	 	 	  case "-m" => generateMakefile(buildFile)
	 	  }
	  }
	  else displayError("Arguments (require 0, 1 or 2)")
  }
  // Load and delegate parse and execution of build file
  def doBuild(buildFile: String): Unit = {
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
	 	  val bldPsr = new GauldiBuildParser(buildConf)
	 	  println(bldPsr.getBuildString()) // DEBUG!
	 	  println(bldPsr.getPreamble())
	 	  println(bldPsr.getBuildSteps())
	 	  println(bldPsr.getInstallSteps())
	 	  println(bldPsr.getCleanSteps())
	  }
  }
  def generateNativeFile(): Unit = {
	  
  }
  def generateMakefile(buildFile: String): Unit = {
	  
  }
  def displayError(ex: Exception): Unit = {
	  println("\nError with: " + ex.getMessage())
	  displayUsage()
  }
  // Overloaded for String parameter
  def displayError(ex: String): Unit = {
	  println("\nError with: " + ex)
	  displayUsage()
  }
  def displayUsage(): Unit = {
	  displayInfo()
	  System.exit(-1)
  }
  def displayInfo(): Unit = {
	  println("\nGauldi platform agnostic build tool")
	  println("Copyright (c) 2010 Sam Saint-Pettersen")
	  println("\nReleased under the MIT License.\n")
  }
}