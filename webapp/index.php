<?php
include_once("config.php");

?>
<!DOCTYPE html>
<html>
<head>
	<meta charset="UTF-8">
	<title><?php echo $APP_TITLE_SHORT; ?></title>
	<link rel="stylesheet" href="css/styles.css">
	<link rel="shortcut icon" href="http://www.latrobe.edu.au/favicon.ico" />
</head>
<body>
	<h1><?php echo $APP_TITLE_LONG; ?></h1>
	<hr class="rule"/>
	<div class="links"><ul><li>Home</li></ul></div>
	<hr class="rule"/>

	<div class="linkgroup">
		<div class="linksect"><a href="barcoder.php">Step 1: Barcoder</a></div>
		<div class="descsect">A tool to replace columns of an alignment with 10 amino acid barcode sequences</div>
	</div>

	<div class="linkgroup">
		<div class="linksect"><a href="reconstructer_jobid.php">Step 2: Reconstructer</a></div>
		<div class="descsect">A tool to restore barcoded alignment columns to their original sequence</div>
	</div>

	<hr class="rule"/>

	<div class="linkgroup">
		<div class="linksect"><a href="https://github.com/TS404/CysBar">Script Downloads</a></div>
		<div class="descsect">You can download the scripts used on this website from our GitHub repository</div>
	</div>

	<hr class="rule"/>
	<div class="footerimgs">
		<div class="leftimg"><a href="http://www.hexima.com.au/"><img src="img/hexima.png" height="80px" alt="Hexima Logo" /></a></div>
		<div class="rightimg"><a href="http://www.latrobe.edu.au/lims/"><img src="img/lims.png" height="80px" alt="LIMS Logo" /></a></div>
	</div>
	<p class="footer">Developed by Thomas Shafee</p>
</body>
</html>
