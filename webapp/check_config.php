<html>
<head><title>Check configuration options are ok</title></head>
<style type="text/css">
span.pass {color: green;}
span.fail {color: red; font-weight: bold;}
</style>
<body>
<ul>
<?php

include_once("config.php");
include_once("support.php");

// check config
$configok = TRUE;
if (is_dir("$BASEDIR")) {
	print "<li>Base directory exists: <span class=\"pass\">OK</span></li>";
} else {
	print "<li>Base directory exists: <span class=\"fail\">FAILED</span></li>";
	$configok = FALSE;
}
if (is_dir("$BIN_DIR")) {
	print "<li>Bin directory exists: <span class=\"pass\">OK</span></li>";
} else {
	print "<li>Bin directory exists: <span class=\"fail\">FAILED</span></li>";
	$configok = FALSE;
}
if (is_writeable("$BIN_DIR")) {
	print "<li>Bin directory writable: <span class=\"fail\">YES (BAD!)</span></li>";
	$configok = FALSE;
} else {
	print "<li>Bin directory writable: <span class=\"pass\">NO (GOOD)</span></li>";
}
if (is_file("$BIN_DIR/Barcoder.sh")) {
	print "<li>Barcoder program exists: <span class=\"pass\">OK</span></li>";
} else {
	print "<li>Barcoder program exists: <span class=\"fail\">FAILED</span></li>";
	$configok = FALSE;
}
if (is_executable("$BIN_DIR/Barcoder.sh")) {
	print "<li>Barcoder program executable: <span class=\"pass\">OK</span></li>";
} else {
	print "<li>Barcoder program executable: <span class=\"fail\">FAILED</span></li>";
	$configok = FALSE;
}
if (is_writeable("$BIN_DIR/Barcoder.sh")) {
	print "<li>Barcoder program writable: <span class=\"fail\">YES (BAD!)</span></li>";
	$configok = FALSE;
} else {
	print "<li>Barcoder program writable: <span class=\"pass\">NO (GOOD)</span></li>";
}
if (is_file("$BIN_DIR/Reconstructer.sh")) {
	print "<li>Reconstructer program exists: <span class=\"pass\">OK</span></li>";
} else {
	print "<li>Reconstructer program exists: <span class=\"fail\">FAILED</span></li>";
	$configok = FALSE;
}
if (is_executable("$BIN_DIR/Reconstructer.sh")) {
	print "<li>Reconstructer program executable: <span class=\"pass\">OK</span></li>";
} else {
	print "<li>Reconstructer program executable: <span class=\"fail\">FAILED</span></li>";
	$configok = FALSE;
}
if (is_writeable("$BIN_DIR/Reconstructer.sh")) {
	print "<li>Reconstructer program writeable: <span class=\"fail\">YES (BAD!)</span></li>";
	$configok = FALSE;
} else {
	print "<li>Reconstructer program writeable: <span class=\"pass\">NO (GOOD)</span></li>";
}
if (is_dir("$RESULT_DIR")) {
	print "<li>Results directory exists: <span class=\"pass\">OK</span></li>";
} else {
	print "<li>Results directory exists: <span class=\"fail\">FAILED</span></li>";
	$configok = FALSE;
}
if (is_writeable("$RESULT_DIR")) {
	print "<li>Results writeable: <span class=\"pass\">OK</span></li>";
} else {
	print "<li>Results writeable: <span class=\"fail\">FAILED</span></li>";
	$configok = FALSE;
}

// print overall status so can use for nagios or other monitoring tool
if ($configok) {
	print "<li>Config OK: <span class=\"pass\">YES</span></li>";
	print "<!-- Config OK: YES -->"; // DO NOT EDIT THIS LINE
} else {
	print "<li>Config OK: <span class=\"fail\">NO!</span></li>";
	print "<!-- Config OK: NO! -->"; // DO NOT EDIT THIS LINE
}

?>
</ul>
</body>
</html>
