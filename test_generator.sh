#!/bin/sh

if ! [ $# -eq 1 ]; then
    echo "Usage: test_generator.sh [generator name]"
    exit 1
fi

NAME=$1

if ! [ `echo "$NAME" | grep generators` ]; then
    NAME="generators/$NAME"
fi

if ! [ `echo "$NAME" | grep '.py'` ]; then
    NAME="$NAME.py"
fi

if ! [ -f "$NAME" ]; then
    echo "missing generator $NAME"
    exit 2
fi

./generators/process_interface.py print $NAME > /tmp/out.svg && inkview /tmp/out.svg

exit 0