#!/bin/sh

# TODO: all model files should be fixed to work with this...

test() {
    # echo "Testing $1"
    PYTHONPATH=$PWD python2.5 $1
}

if [ $# -ne 0 ]; then
    if [ -f $1 ]; then
	test $1
	exit 0
    else
	echo "Missing file: $1"
	exit 2
    fi
fi

for python_file in `ls model | grep '\.py$'`; do
    test model/$python_file
done

exit 0
