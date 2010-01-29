#!/bin/sh

DEFAULT_URL="http://beauty-bar.appspot.com/chart"
DEFAULT_STYLE="default"
DEFAULT_DIM="300x200"
DEFAULT_OUTPUT="chart.svg"

usage() {
    echo "Usage: beauty-bar.sh [OPTIONS] title=value title=value ..."
    echo 
    echo "Required six (6) title=value pairs and optional arguments"
    echo "  -u\tUrl to chart api, default: $DEFAULT_URL"
    echo "  -n\tStyle name for chart, default: $DEFAULT_STYLE"
    echo "  -s\tSize for output image, default: $DEFAULT_DIM"
    echo "  -v\tViewer which is chart image is opened, no default"
    echo "  -o\tOutput file not used with viewer, default: $DEFAULT_OUTPUT"
    echo "  -f\tForce, overwrite existing file"
    echo
    echo "Example: beauty-bar.sh -n nature a=10 b=15 c=20 d=30 e=40 f=50"
    exit 1
}

URL=$DEFAULT_URL
CHT=$DEFAULT_STYLE
CHS=$DEFAULT_DIM
OUTPUT=$DEFAULT_OUTPUT

while getopts "u:n:s:v:o:f" flag; do
    case $flag in
	u) URL=$OPTARG ;;
	n) CHT=$OPTARG ;;
	s) CHS=$OPTARG ;;
	v) VIEWER=$OPTARG ;;
	o) OUTPUT=$OPTARG ;;
	f) FORCE=1 ;;
	[?]) usage ;;
    esac
done
shift `expr $OPTIND - 1`

if [ $# -ne 6 ]; then
    usage
fi

CHD=""
CHL=""

# unpack values to arrays
while [ $# -ne 0 ]; do
    NAME=`echo $1 | cut -d = -f 1`
    VALUE=`echo $1 | cut -d = -f 2`
    CHD="$CHD,$VALUE"
    CHL="$CHL|$NAME"
    shift
done

# remove trailing commas and pipes
CHD=`echo $CHD | cut -c 2-`
CHL=`echo $CHL | cut -c 2-`

if [ "x$VIEWER" = "x" ]; then
    if [ -f "$OUTPUT" ]; then
	if [ "x$FORCE" = "x" ]; then 
	    echo "error, file $OUTPUT already exists"
	    exit 2
	else
	    rm $OUTPUT
	fi
    fi
else
    OUTPUT=`mktemp`
fi

# get file
wget -q --tries=3 -O $OUTPUT $URL?cht=$CHT&chd=t:$CHD&chs=$CHS&chl=$CHL

# lets hope it is there, as it seems to take some time to get it there
# and we don't want to "sleep 1" just for that.
# if ! [ -f "$OUTPUT" ]; then
#    echo "Couldn't connect url: $URL?cht=$CHT&chd=t:$CHD&chs=$CHS&chl=$CHL"
#    exit 3
# fi

if [ "x$VIEWER" = "x" ]; then
    echo "Saved as $OUTPUT"
else
    $VIEWER $OUTPUT
fi

exit 0