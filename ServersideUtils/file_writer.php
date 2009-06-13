<?php
//
// File writer utility
// Dynamically write files from provided data to a server cache.
// UUIDs are generated by uuid_generator script available here:
// 
// Call like this with an Ajax request:
// http://[your.server]/[path.to]/file_writer.php?prj=[your.project]
// &out=[output.dir]&data=[data.to.write]&ext=[file.extension]
// 
// Copyright (c) 2009 Sam Saint-Pettersen.
// 
// Released under the MIT license.
//
require_once "uuid_generator.php";

function fileWriter($prj, $out, $src, $data, $ext) {
	// Generate UUID suffix for file
	$uuid = uuid();
	// Write out the file to the source cache folder
	$fh = fopen($prj . $out . $src . '_' . $uuid . '.' . $ext, 'w');
	fwrite($fh, $data); // TODO Change to write line by line
	fclose($fh);
	// Return relative path to calling code (echo)
	echo $out . $src . '_' . $uuid . '.' . $ext; 
}
fileWriter($_GET['prj'], $_GET['out'], $_GET['src'], $_GET['data'], $_GET['ext']);
?>
