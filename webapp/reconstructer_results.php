<?php 
session_start();
include_once("config.php");
include_once("support.php");

$jobid=san_jobid($_GET['j']);

if ($jobid == "" || !is_dir("$RESULT_DIR/$jobid") || !is_file("$RESULT_DIR/$jobid/$PARAM_FILE"))
{
    $_SESSION['msg'] = "Failed to find your job details.  Please try again and if that fails contact the system admin.";

    //header("location: reconstructer_jobid3.php");
}

?>
<!DOCTYPE html>
<html>
<head>
	<meta charset="UTF-8">
	<title>Reconstructer results - <?php echo $APP_TITLE_SHORT; ?></title>
	<link rel="stylesheet" href="css/styles.css">
	<link rel="shortcut icon" href="http://www.latrobe.edu.au/favicon.ico" />
</head>
<body>
	<h1><?php echo $APP_TITLE_LONG; ?></h1>
	<hr class="rule"/>
	<div class="links"><ul><li><a href="./">Home</a></li><li> &gt; <a href="reconstructer.php">Reconstructer</a></li><li> &gt; Results</li></ul></div>
	<hr class="rule"/>
	
<?php
    if (isset($_SESSION['msg'])) {
?>
    <div class="errormsg"><?php print $_SESSION['msg']; ?></div>
<?php
    }
    unset($_SESSION['msg']);
?>

	<h2>Results</h2>
	<div class="results">
	    <div class="headertext">This alignment has had the barcodes removed and the original amino acids restored</div>
		<table class="results">
		<tbody>
		    <tr>
		        <th class="headingcol heading">Job Number:</th>
		        <td><?php echo $jobid; ?></td>
		    </tr>
		    <tr>
		        <th class="heading">Aligned sequences:</th>
		        <td><a href="download_align.php?j=<?php echo $jobid; ?>">Download [FastA]</a></td>
		    </tr>
		    <tr>
		        <td colspan="2"><textarea class="results" readonly="readonly"><?php if (is_readable("$RESULT_DIR/$jobid/FINAL_ALIGNMENT.fa")) { readfile("$RESULT_DIR/$jobid/FINAL_ALIGNMENT.fa"); }
else { print "No results found, please contact the system administrator"; } ?></textarea></td>
		    </tr>
		    <tr>
		        <th class="heading">Loop statistics:</th>
		        <td><a href="download_stats.php?j=<?php echo $jobid; ?>">Download [CSV]</a></td>
		    </tr>
		    <tr>
		        <td colspan="2"><textarea class="results" readonly="readonly"><?php if (is_readable("$RESULT_DIR/$jobid/Loop_statistics.csv")) { readfile("$RESULT_DIR/$jobid/Loop_statistics.csv"); }
else { print "No results found, please contact the system administrator"; } ?></textarea></td>
		    </tr>
		</tbody>
		</table>
	</div>
	<h2>Analysis</h2>
	<div class="analysis">
		<table class="results">
		<tbody>
		    <tr>
		        <th class="headingcol heading">Analysis spreadsheet:</th>
		        <td><a href="assets/loopproperties.xlsx">Download [XLSX]</a></td>
		    </tr>
		</tbody>
		</table>
	</div>
	<hr class="rule"/>
	<div class="footerimgs">
		<div class="leftimg"><a href="http://www.hexima.com.au/"><img src="img/hexima.png" height="80px" alt="Hexima Logo" /></a></div>
		<div class="rightimg"><a href="http://www.latrobe.edu.au/lims/"><img src="img/lims.png" height="80px" alt="LIMS Logo" /></a></div>
	</div>
	<p class="footer">Developed by Thomas Shafee</p>
</body>
</html>

