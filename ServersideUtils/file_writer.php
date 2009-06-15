<?php
//
// File writer utility (PHP implementation)
// Dynamically write files from provided data to a server cache.
// 
// Call with this URL with a returning Ajax request:
// http://[your.server]/[path.to]/file_writer.php?out=
// [output.path.relative.to.script.position]
// &data=[raw.encoded.data.to.write]&ext=[file.extension]
// 
// Copyright (c) 2009 Sam Saint-Pettersen.
// 
// Released under the MIT license.
//
// UUIDs suffixes for files are generated by uuid_generator script 
// available at http://www.somacon.com/p113.php (copy script text)
//
require_once "../lib/uuid_generator.php";

function fileWriter($out, $data, $ext) {
	// Generate UUID suffix for file
	$uuid = uuid();
	// When all parameters are passed when invoking...
	if($prj != null or $out != null or $data != null or $ext != null) {
		// Write out the file to the output folder
		$nfile = $out . '_' . $uuid . '.' . $ext;
		$fh = fopen($nfile, 'w');
		fwrite($fh, str_replace('\\', '', $data));
		fclose($fh);
		// Return relative path to file to calling code (echo)
		echo $nfile;
	// Otherwise, return insufficient parameters message to calling code (echo)
	} else echo 'Error: Insufficient parameters given.';
}
fileWriter($_GET['out'], $_GET['data'], $_GET['ext']);
?>
