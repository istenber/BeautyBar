#!/bin/sh

DPI=10
PROG=$0

if [ $# -eq 0 ]; then
    NAME=`basename $PROG`
    echo "Usage: $NAME <SVG file>"
    exit 1
fi

if [ $1 = "all" ]; then
    echo "Converting all SVG files in directory"
    FILES=`ls *.svg`
    for file in $FILES; do
	$PROG $file
    done
    exit 0
fi

SVG_FILE=$1
PNG_FILE=`echo $SVG_FILE | sed 's/\.svg$/\.png/'`

echo "Converting $SVG_FILE to $PNG_FILE"

inkscape --export-dpi=$DPI --export-png=$PNG_FILE $SVG_FILE > /dev/null 2>&1
