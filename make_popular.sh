#!/bin/sh

if [ $# -ne 2 ]; then
    echo "Usage: make_popular.sh [svg file] [name]"
    exit 1
fi

FILE=$1
NAME=$2

if ! [ -f "$FILE" ]; then
    echo "$FILE is not file?"
    exit 2
fi

OUTFILE="$NAME.png"

if [ -e $OUTFILE ]; then
    echo "$OUTFILE exists already"
    exit 3
fi

TMPFILE=/tmp/tmp-`basename $FILE`

cat "$FILE" | sed -e 's/xlink:href=\"\/dbimages\//xlink:href=\"\/home\/ippe\/dev\/beautybar\/dynamic_images\//g' -e "s/<\/svg>/<g><text style=\"font-family:Arial;fill:none;stroke-width:5px;stroke:#000000;text-anchor:middle;font-weight:bold;\" font-size=\"50\" y=\"125\" x=\"150\">$NAME<\/text><text style=\"font-family:Arial;fill:#ffffff;text-anchor:middle;font-weight:bold;\" font-size=\"50\" stroke=\"none\" y=\"125\" x=\"150\">$NAME<\/text><\/g><\/svg>/" > $TMPFILE

inkscape $TMPFILE -z -a 0:0:300:200 -h 150 -e $OUTFILE > /dev/null 2>&1

echo "made $OUTFILE"

exit 0
