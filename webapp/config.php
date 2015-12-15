<?php

# BASEDIR of the application
$BASEDIR="/var/www/html";

$WEB_LOG="/var/log/httpd/access_log";
$WEB_ERRLOG="/var/log/httpd/error_log";

# the directory containing the barcoder and reconstructer scripts
# relative to results dir (or could be full path)
$BIN_DIR="$BASEDIR/bin";

# directory to store result files for the users
$RESULT_DIR="$BASEDIR/results";

# config options
$PARAM_FILE="config.txt";

# the file the barcode values are writen to (in each result directory)
$BARCODE_FILE="barcodes.txt";

# barcoding sequence filenames (in each result directory)
$BARCODE_INPUTFILE="source.fa";
$BARCODE_OUTPUTFILE="barcoded.fa";

# reconstruction sequences filenames (as expected by reconstructer.sh)
$RECON_INPUTFILE="align.fa";
$RECON_OUTPUTFILE="recon.fa";
$RECON_STATSFILE="loopstats.csv";

$APP_TITLE_SHORT="CysBar online";
$APP_TITLE_LONG="CysBar protein alignment accessory tools";

# size in bytes of maximum size of sequences per run
$MAX_SEQ_SIZE=1048576;

?>
