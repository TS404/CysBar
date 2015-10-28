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

# source sequence filename (as expected by barcoder.sh)
$SRC_SEQ_FILE="source.fa";

# the file the c and barcode values are writen to (in each result directory)
$PARAM_FILE="params.txt";

# aligned sequences filename (as expected by reconstructer.sh)
$ALIGN_SEQ_FILE="align.fa";

$APP_TITLE_SHORT="Protein alignment accessory tools";
$APP_TITLE_LONG="Barcoder and Reconstructer protein alignment accessory tools";

# size in bytes of maximum size of sequences per run
$MAX_SEQ_SIZE=1048576;

?>
