<?php
// This page processes reconstructer requests and redirects to reconstructer_results.php
session_start();
include_once("config.php");
include_once("support.php");

$jobid=san_jobid($_POST['j']);

if ($jobid == "" || !is_dir("$RESULT_DIR/$jobid") || !is_file("$RESULT_DIR/$jobid/$PARAM_FILE"))
{
    $_SESSION['msg'] = "Failed to find your job details.  Please try again and if that fails contact the system admin.";

    header("location: reconstructer_jobid.php");
    exit();
}

// load job details from file
$params = array_map("trim", file("$RESULT_DIR/$jobid/$PARAM_FILE"));
$c = array_slice($params, 0, 8);
$bc = array_slice($params, 8, 8);

if (count($c) != 8 || count($bc) != 8)
{
    $_SESSION['msg'] = "Failed to find your job details.  Please try again and if that fails contact the system admin.";

    header("location: reconstructer_jobid.php");
    exit();
}

// sanitise input parameters
$seq = san_seq($_POST['seq']);

if (strlen($seq) < 4) {
    $_SESSION['msg'] = "Sequence size is too small.  Please enter at least 1 sequence";
    saveVars($_SESSION, $c, $bc, $seq);
    header("location: reconstructer.php?j=$jobid");
    exit();
}

if (strlen($seq) > $MAX_SEQ_SIZE) {
    $SIZE=$MAX_SEQ_SIZE / 1024;
    $_SESSION['msg'] = "Sequence size is too large.  Please limit it to $SIZE kiB total";
    saveVars($_SESSION, $c, $bc, $seq);
    header("location: reconstructer.php?j=$jobid");
    exit();
}

// check config
if (!is_executable("$BIN_DIR/Reconstructer.sh")) {
	$_SESSION['msg'] = "Server configuration error, please contact the system administrator (error num: 2)";
    saveVars($_SESSION, $c, $bc, $seq);
    header("location: reconstructer.php?j=$jobid");
	exit();
}

// write the input files
chdir("$RESULT_DIR/$jobid");
$seqfile = fopen($ALIGN_SEQ_FILE, "w");
fwrite($seqfile, $seq);
fclose($seqfile);

// run the script
$bc = array_map("escapeshellarg", $bc);
$cmd="$BIN_DIR/Reconstructer.sh {$bc[0]} {$bc[1]} {$bc[2]} {$bc[3]} {$bc[4]} {$bc[5]} {$bc[6]} {$bc[7]}";
$output="";
$rc=-1;
exec($cmd, $output, $rc);

// debug info
$_SESSION['jobid']=$jobid;
$_SESSION['cmd']=$cmd;
$_SESSION['output']=$output;
$_SESSION['rc']=$rc;

header("location: reconstructer_results.php?j=${jobid}");
?>
