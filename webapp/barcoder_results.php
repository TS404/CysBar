<?php 
session_start();
include_once("config.php");
include_once("support.php");

$jobid=san_jobid($_GET['j']);

if ($jobid == "" || !is_dir("$RESULT_DIR/$jobid") || !is_file("$RESULT_DIR/$jobid/$PARAM_FILE"))
{
    $_SESSION['msg'] = "Failed to generate your barcoded files.  Please try again and if that fails contact the system admin.";

    header("location: barcoder.php");
    exit();
}



// load job details from file
$params = array_map("trim", file("$RESULT_DIR/$jobid/$PARAM_FILE"));
$c = array_slice($params, 0, 8);
$bc = array_slice($params, 8, 8);

if (count($c) != 8 || count($bc) != 8)
{
    $_SESSION['msg'] = "Failed to generate your barcoded files.  Please try again and if that fails contact the system admin.";

    header("location: barcoder.php");
    exit();
}

?>
<!DOCTYPE html>
<html>
<head>
	<meta charset="UTF-8">
	<title>Barcoder results - <?php echo $APP_TITLE_SHORT; ?></title>
	<link rel="stylesheet" href="css/styles.css">
	<link rel="shortcut icon" href="http://www.latrobe.edu.au/favicon.ico" />
</head>
<body>
	<h1><?php echo $APP_TITLE_LONG; ?></h1>
	<hr class="rule"/>
	<div class="links"><ul><li><a href="./">Home</a></li><li> &gt; <a href="barcoder.php">Barcoder</a></li><li> &gt; Results</li></ul></div>
	<hr class="rule"/>
<?php
    if (isset($_SESSION['msg'])) {
?>
    <div class="errormsg"><?php print $_SESSION['msg']; ?></div>
<?php
    }
    unset($_SESSION['msg']);
?>

		<h2>Parameters</h2>
	<div class="roparams">
		<table>
		<thead>
			<tr>
				<th class="num">#</th>
				<th class="c">C</th>
				<th class="bc">Barcode</th>
			</tr>
		</thead>
		<tbody>
			<tr>
				<td class="num">1</td>
				<td class="c"><input type="text" name="c1" readonly="readonly" value="<?php echo htmlspecialchars($c[0]); ?>"/></td>
				<td class="bc"><input type="text" name="bc1" readonly="readonly" value="<?php echo htmlspecialchars($bc[0]); ?>"/></td>
			</tr>
			<tr>
				<td class="num">2</td>
				<td class="c"><input type="text" name="c2" readonly="readonly" value="<?php echo htmlspecialchars($c[1]); ?>"/></td>
				<td class="bc"><input type="text" name="bc2" readonly="readonly" value="<?php echo htmlspecialchars($bc[1]); ?>"/></td>
			</tr>
			<tr>
				<td class="num">3</td>
				<td class="c"><input type="text" name="c3" readonly="readonly" value="<?php echo htmlspecialchars($c[2]); ?>"/></td>
				<td class="bc"><input type="text" name="bc3" readonly="readonly" value="<?php echo htmlspecialchars($bc[2]); ?>"/></td>
			</tr>
			<tr>
				<td class="num">4</td>
				<td class="c"><input type="text" name="c4" readonly="readonly" value="<?php echo htmlspecialchars($c[3]); ?>"/></td>
				<td class="bc"><input type="text" name="bc4" readonly="readonly" value="<?php echo htmlspecialchars($bc[3]); ?>"/></td>
			</tr>
			<tr>
				<td class="num">5</td>
				<td class="c"><input type="text" name="c5" readonly="readonly" value="<?php echo htmlspecialchars($c[4]); ?>"/></td>
				<td class="bc"><input type="text" name="bc5" readonly="readonly" value="<?php echo htmlspecialchars($bc[4]); ?>"/></td>
			</tr>
			<tr>
				<td class="num">6</td>
				<td class="c"><input type="text" name="c6" readonly="readonly" value="<?php echo htmlspecialchars($c[5]); ?>"/></td>
				<td class="bc"><input type="text" name="bc6" readonly="readonly" value="<?php echo htmlspecialchars($bc[5]); ?>"/></td>
			</tr>
			<tr>
				<td class="num">7</td>
				<td class="c"><input type="text" name="c7" readonly="readonly" value="<?php echo htmlspecialchars($c[6]); ?>"/></td>
				<td class="bc"><input type="text" name="bc7" readonly="readonly" value="<?php echo htmlspecialchars($bc[6]); ?>"/></td>
			</tr>
			<tr>
				<td class="num">8</td>
				<td class="c"><input type="text" name="c8" readonly="readonly" value="<?php echo htmlspecialchars($c[7]); ?>"/></td>
				<td class="bc"><input type="text" name="bc8" readonly="readonly" value="<?php echo htmlspecialchars($bc[7]); ?>"/></td>
			</tr>
		</tbody>
		</table>
	</div>
	
	<h2>Results</h2>
	<div class="results">
	    <div class="headertext">Please copy this Job Number (or bookmark/save this page), you will need it for running the reconstructer tool (to 
	        restore the correct amino acids in place of the barcodes).</div>
		<table class="results">
		<tbody>
		    <tr>
		        <th class="headingcol heading">Job Number:</th>
		        <td><?php echo $jobid; ?></td>
		    </tr>
		    <tr>
		        <th class="heading">Barcoded sequences:</th>
		        <td><a href="download_barcoded.php?j=<?php echo $jobid; ?>">Download [FastA]</a></td>
		    </tr>
		    <tr>
		        <td colspan="2"><textarea class="results" readonly="readonly"><?php if (is_readable("$RESULT_DIR/$jobid/$BARCODE_OUTPUTFILE")) { readfile("$RESULT_DIR/$jobid/$BARCODE_OUTPUTFILE"); }
else { print "No results found, please contact the system administrator"; } ?></textarea></td>
		    </tr>
		</tbody>
		</table>
	</div>
	
	<h2>Reconstructer</h2>
	<div class="reconstructing">
	    <div class="headertext">This barcoded alignment can be re-aligned using any standard alignment program. 
	        The barcoded columns will be constrained, whilst the sequences in between are free to re-align.</div>
	    <table class="results">
		<tbody>
		    <tr>
		        <th class="headingcol heading">Reconstruction link:</th>
		        <td><a href="reconstructer.php?j=<?php echo $jobid; ?>">Reconstruct (<?php echo $jobid; ?>)</a></td>
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

