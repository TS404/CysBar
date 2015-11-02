#!/bin/bash

MAXAGE=7
RESULTDIR=/var/www/html/tshafee/results


# delete result directories older than maxage
find $RESULTDIR/* -maxdepth 1 -mtime +$MAXAGE -type d -print | xargs rm -rf

## EOF ##

