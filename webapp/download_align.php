<?php
session_start();
include_once("config.php");
include_once("support.php");

$jobid=san_jobid($_GET['j']);

$file="$RESULT_DIR/$jobid/$RECON_OUTPUTFILE";

if ($jobid == "" || !is_dir("$RESULT_DIR/$jobid") || !is_file($file))
{
    $_SESSION['msg'] = "Failed to find your job results.  Please try again and if that fails contact the system admin.";

    header("location: reconstructer.php");
}
header('Content-Description: File Transfer');
header('Content-Type: text/plain'); //text/csv
header('Content-Disposition: attachment; filename='.basename($file));
header('Expires: 0');
header('Cache-Control: must-revalidate');
header('Pragma: public');
header('Content-Length: ' . filesize($file));
readfile($file);
exit;

?>
