#!/bin/sh

BROWSERS="firefox opera google-chrome ie6 epiphany konqueror safari"

if [ $# -eq 0 ]; then
    echo "Usage: test-browser.sh [browser]"
    echo " where browser is one of following:"
    echo " $BROWSERS"
    exit 1
fi

# versions?
# ie6, ie7, ie8, ie9
# firefox2, firefox3 firefox3.5
# safari3, safari4
# operating systems: linux, mac, freebsd, windows
# non-graphical? links?
# svg plugins? adobe

RUNNING=`ps a | grep [d]ev_appserver.py`
if [ "x$RUNNING" = "x" ]; then
    echo "Dev server is not running."
    exit 3
fi

BROWSER=$1

for c in $BROWSERS; do
    if [ "x$c" = "x$BROWSER" ]; then
	if [ "x$BROWSER" = "xkonqueror" ] || [ "x$BROWSER" = "xsafari" ]; then
	    echo "Safari and Konqueror are not yet supported."
	    exit 3
	fi
	echo "Testing with $BROWSER"
	$BROWSER http://localhost:8080 &
	exit 0
    fi
done

echo "Unknown browser: $BROWSER"
exit 2