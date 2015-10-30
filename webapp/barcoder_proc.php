<?php

session_start();

include_once("config.php");
include_once("support.php");

/// This page processes barcoder requests and redirects to barcoder_results.php ///

// sanitise the input

$c = array(san_c($_POST['c1']),san_c($_POST['c2']),san_c($_POST['c3']),san_c($_POST['c4']),
            san_c($_POST['c5']),san_c($_POST['c6']),san_c($_POST['c7']),san_c($_POST['c8']));

$bc = array(san_barcode($_POST['bc1']),san_barcode($_POST['bc2']),san_barcode($_POST['bc3']),san_barcode($_POST['bc4']),
            san_barcode($_POST['bc5']),san_barcode($_POST['bc6']),san_barcode($_POST['bc7']),san_barcode($_POST['bc8']));

if ($c[0]=="0") $bc[0]="";
if ($c[1]=="0") $bc[1]="";
if ($c[2]=="0") $bc[2]="";
if ($c[3]=="0") $bc[3]="";
if ($c[4]=="0") $bc[4]="";
if ($c[5]=="0") $bc[5]="";
if ($c[6]=="0") $bc[6]="";
if ($c[7]=="0") $bc[7]="";


$seq = san_seq($_POST['seq']);

if ($c[0]=="0") {
    $_SESSION['msg'] = "No substitutions requested.  Please enter at least 1 value for 'c' and 'barcode'";
    saveVars($_SESSION, $c, $bc, $seq);
    header("location: barcoder.php");
    exit();
}

if (strlen($seq) < 4) {
    $_SESSION['msg'] = "Sequence size is too small.  Please enter at least 1 sequence";
    saveVars($_SESSION, $c, $bc, $seq);
    header("location: barcoder.php");
    exit();
}

if (strlen($seq) > $MAX_SEQ_SIZE) {
    $SIZE=$MAX_SEQ_SIZE / 1024;
    $_SESSION['msg'] = "Sequence size is too large.  Please limit it to $SIZE kiB total";
    saveVars($_SESSION, $c, $bc, $seq);
    header("location: barcoder.php");
    exit();
}

for ($i = 0; $i < 8; $i++) {
    if (strlen($bc[$i]) < 1 && $c[$i] != "0") {
        $_SESSION['msg'] = "Please enter a barcode for each residue to replace";
        saveVars($_SESSION, $c, $bc, $seq);
        header("location: barcoder.php");
        exit();
    }
}

// check config
if (!is_executable("$BIN_DIR/cysbar")) {
	$_SESSION['msg'] = "Server configuration error, please contact the system administrator (1)";
        saveVars($_SESSION, $c, $bc, $seq);
    header("location: barcoder.php");
	exit();
}


// generate a unique id
$i = 0;
do {
    $strong = true;
    $jobid=bin2hex(openssl_random_pseudo_bytes(16, $strong));
    $i++;
} while(file_exists("$RESULT_DIR/$jobid") && $i < 100);
if ($i >= 100) {
    $_SESSION['msg'] = "Failed to generate your barcoded files.  Please try again and if that fails contact the system admin. (2)";
    saveVars($_SESSION, $c, $bc, $seq);
    header("location: barcoder.php");
    exit();
}

// make the directory
if (!mkdir("$RESULT_DIR/$jobid", 0755, true)) {
    $_SESSION['msg'] = "Failed to generate your barcoded files.  Please try again and if that fails contact the system admin. (3)";
        saveVars($_SESSION, $c, $bc, $seq);
    header("location: barcoder.php");
    exit();
}

// write the input files
//echo getcwd();
chdir("$RESULT_DIR/$jobid");
$seqfile = fopen($BARCODE_INPUTFILE, "w");
fwrite($seqfile, $seq);
fclose($seqfile);

// write settings for display
$paramfile = fopen($PARAM_FILE, "w");
fwrite($paramfile, "{$c[0]}\n");
fwrite($paramfile, "{$c[1]}\n");
fwrite($paramfile, "{$c[2]}\n");
fwrite($paramfile, "{$c[3]}\n");
fwrite($paramfile, "{$c[4]}\n");
fwrite($paramfile, "{$c[5]}\n");
fwrite($paramfile, "{$c[6]}\n");
fwrite($paramfile, "{$c[7]}\n");
fwrite($paramfile, "{$bc[0]}\n");
fwrite($paramfile, "{$bc[1]}\n");
fwrite($paramfile, "{$bc[2]}\n");
fwrite($paramfile, "{$bc[3]}\n");
fwrite($paramfile, "{$bc[4]}\n");
fwrite($paramfile, "{$bc[5]}\n");
fwrite($paramfile, "{$bc[6]}\n");
fwrite($paramfile, "{$bc[7]}\n");
fclose($paramfile);


// write barcodes (for later reconstruction)
$paramfile = fopen($BARCODE_FILE, "w");
for ($i = 0; $i < 8; $i++) {
	if ($bc[$i] != "")
		fwrite($paramfile, "{$bc[$i]}\n");
}
fclose($paramfile);


// run the script
//$c = array_map("escapeshellarg", $c);

// format positions
$pos = "";
for ($i = 0; $i < 8; $i++) {
	if ($c[$i] != "0" && $c[$i] !== 0) {
		$pos .= " -b {$c[$i]}";
	}
}

// Redirect errors to /dev/null - code requires that awk error on null values, doesn't populate 'columns' files, and reconstructions works.  Bad!  No Donut!
// $cmd="$BIN_DIR/cysbar {$c[0]} {$c[1]} {$c[2]} {$c[3]} {$c[4]} {$c[5]} {$c[6]} {$c[7]} {$bc[0]} {$bc[1]} {$bc[2]} {$bc[3]} {$bc[4]} {$bc[5]} {$bc[6]} {$bc[7]} 2>/dev/null";
$cmd="$BIN_DIR/cysbar -B {$BARCODE_FILE} {$pos} {$BARCODE_INPUTFILE} >{$BARCODE_OUTPUTFILE} 2>barcode-errors.log";
//$cmd="ls -la";
$output="";
$rc=-1;
exec($cmd, $output, $rc);

$_SESSION['jobid']=$jobid;
$_SESSION['cmd']=$cmd;
$_SESSION['output']=$output;
$_SESSION['rc']=$rc;

header("location: barcoder_results.php?j=${jobid}");
?>
