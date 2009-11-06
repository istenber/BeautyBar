#!/bin/sh

# change Inkscape produced svg image to use static images from /images folder

FILE=template.svg
TMP=$FILE.tmp

cat $FILE | sed -e 's/xlink:href="paper\.jpg"/xlink:href="\/images\/paper\.jpg"/' > $TMP
if [ "x$?" = "x0" ]; then
    mv $TMP $FILE
    echo "ok."
else
    echo "failed."
fi
