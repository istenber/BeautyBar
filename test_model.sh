#!/bin/sh

# TODO: all model files should be fixed to work with this...

PYTHONPATH=$PWD python2.5 model/data.py
exit 0

for python_file in `ls model | grep '\.py$'`; do
  # echo "Testing $python_file"
  PYTHONPATH=$PWD python2.5 model/$python_file
done
