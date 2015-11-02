<?php 
session_start();
include_once("config.php");
include_once("support.php");
?>
<!DOCTYPE html>
<html>
<head>
	<meta charset="UTF-8">
	<title>Barcoder - <?php echo $APP_TITLE_SHORT; ?></title>
	<link rel="stylesheet" href="css/styles.css">
	<link rel="shortcut icon" href="http://www.latrobe.edu.au/favicon.ico" />
</head>
<body>
	<h1><?php echo $APP_TITLE_LONG; ?></h1>
	<hr class="rule"/>
	<div class="links"><ul><li><a href="./">Home</a></li><li> &gt; Logs </li></ul></div>
	<hr class="rule"/>
	<div class="headertext"><strong>Description</strong>: Log viewer for 'barcoder' app - shows web logs</div>

<?php
    if (isset($_SESSION['msg'])) {
?>
    <div class="errormsg"><?php print $_SESSION['msg']; ?></div>
<?php
    }
    unset($_SESSION['msg']);
?>

<pre>
<?php readfile("$WEB_ERRLOG"); ?>
</pre>
	<hr class="rule"/>
	<div class="footerimgs">
		<div class="leftimg"><a href="http://www.hexima.com.au/"><img src="img/hexima.png" height="80px" alt="Hexima Logo" /></a></div>
		<div class="rightimg"><a href="http://www.latrobe.edu.au/lims/"><img src="img/lims.png" height="80px" alt="LIMS Logo" /></a></div>
	</div>
	<p class="footer">Developed by Thomas Shafee</p>
</body>
</html>

