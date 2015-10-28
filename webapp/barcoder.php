<?php 
session_start();
include_once("config.php");
include_once("support.php");

$c1 = popKey($_SESSION, 'c1', 0);
$c2 = popKey($_SESSION, 'c2', 0);
$c3 = popKey($_SESSION, 'c3', 0);
$c4 = popKey($_SESSION, 'c4', 0);
$c5 = popKey($_SESSION, 'c5', 0);
$c6 = popKey($_SESSION, 'c6', 0);
$c7 = popKey($_SESSION, 'c7', 0);
$c8 = popKey($_SESSION, 'c8', 0);
$bc1= popKey2($_SESSION, 'bc1', "pmhmmwphmmhw");
$bc2= popKey2($_SESSION, 'bc2', "mwhmmhwhhhmw");
$bc3= popKey2($_SESSION, 'bc3', "hmhwhwmmhwmw");
$bc4= popKey2($_SESSION, 'bc4', "wwpmhwppkmwh");
$bc5= popKey2($_SESSION, 'bc5', "pphhwmphwmmh");
$bc6= popKey2($_SESSION, 'bc6', "mwwhmhphpphw");
$bc7= popKey2($_SESSION, 'bc7', "hwmpmhwpmmwh");
$bc8= popKey2($_SESSION, 'bc8', "pmwhwwhhpwmm");
$seq= popKey($_SESSION, 'seq', "");
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
	<div class="links"><ul><li><a href="./">Home</a></li><li> &gt; Barcoder</li></ul></div>
	<hr class="rule"/>
	<div class="headertext"><strong>Description</strong>: This tool replaces columns of an alignment with 12 amino acid barcode sequences. Barcoding cysteines prevents their misalignment in cystine-rich, highly divergent sequences.</div>
	<div class="headertext"><strong>Instructions</strong>: Paste the sequence alignment (fasta format) into the box below. Specify the alignment columns to be barcoded. Default barcode sequences can be changed if desired. The output alignment from this tool can be re-aligned using any standard alignment tool with the barcoded columns constrianed to align. Please save the Job Number for later use in the reconstructer tool.</div>

<?php
    if (isset($_SESSION['msg'])) {
?>
    <div class="errormsg"><?php print $_SESSION['msg']; ?></div>
<?php
    }
    unset($_SESSION['msg']);
?>

	<form method="POST" action="barcoder_proc.php">
	<div class="params">
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
				<td class="c"><input type="text" name="c1" value="<?php echo htmlspecialchars($c1); ?>"/></td>
				<td class="bc"><input type="text" name="bc1" maxlength="12" value="<?php echo htmlspecialchars($bc1); ?>"/></td>
			</tr>
			<tr>
				<td class="num">2</td>
				<td class="c"><input type="text" name="c2" value="<?php echo htmlspecialchars($c2); ?>"/></td>
				<td class="bc"><input type="text" name="bc2" maxlength="12" value="<?php echo htmlspecialchars($bc2); ?>"/></td>
			</tr>
			<tr>
				<td class="num">3</td>
				<td class="c"><input type="text" name="c3" value="<?php echo htmlspecialchars($c3); ?>"/></td>
				<td class="bc"><input type="text" name="bc3" maxlength="12" value="<?php echo htmlspecialchars($bc3); ?>"/></td>
			</tr>
			<tr>
				<td class="num">4</td>
				<td class="c"><input type="text" name="c4" value="<?php echo htmlspecialchars($c4); ?>"/></td>
				<td class="bc"><input type="text" name="bc4" maxlength="12" value="<?php echo htmlspecialchars($bc4); ?>"/></td>
			</tr>
			<tr>
				<td class="num">5</td>
				<td class="c"><input type="text" name="c5" value="<?php echo htmlspecialchars($c5); ?>"/></td>
				<td class="bc"><input type="text" name="bc5" maxlength="12" value="<?php echo htmlspecialchars($bc5); ?>"/></td>
			</tr>
			<tr>
				<td class="num">6</td>
				<td class="c"><input type="text" name="c6" value="<?php echo htmlspecialchars($c6); ?>"/></td>
				<td class="bc"><input type="text" name="bc6" maxlength="12" value="<?php echo htmlspecialchars($bc6); ?>"/></td>
			</tr>
			<tr>
				<td class="num">7</td>
				<td class="c"><input type="text" name="c7" value="<?php echo htmlspecialchars($c7); ?>"/></td>
				<td class="bc"><input type="text" name="bc7" maxlength="12" value="<?php echo htmlspecialchars($bc7); ?>"/></td>
			</tr>
			<tr>
				<td class="num">8</td>
				<td class="c"><input type="text" name="c8" value="<?php echo htmlspecialchars($c8); ?>"/></td>
				<td class="bc"><input type="text" name="bc8" maxlength="12" value="<?php echo htmlspecialchars($bc8); ?>"/></td>
			</tr>
		</tbody>
		</table>
	</div>
	<div class="seq">
		<label for="seq">FastA sequences</label>
		<textarea id="seq" name="seq" class="seq"><?php echo htmlspecialchars($seq); ?></textarea>
	</div>
	<div class="control">
		<div class="submittext">The job should take no longer than a few minutes</div>
		<input type="submit" class="defaultsubmit" value="Barcode Sequences"/>
	</div>
	</form>

	<hr class="rule"/>
	<div class="footerimgs">
		<div class="leftimg"><a href="http://www.hexima.com.au/"><img src="img/hexima.png" height="80px" alt="Hexima Logo" /></a></div>
		<div class="rightimg"><a href="http://www.latrobe.edu.au/lims/"><img src="img/lims.png" height="80px" alt="LIMS Logo" /></a></div>
	</div>
	<p class="footer">Developed by Thomas Shafee</p>
</body>
</html>

