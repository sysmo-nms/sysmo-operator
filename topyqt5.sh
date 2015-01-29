#!/bin/sh

A=`find . -name "*.py"`

T="tmpfile"
for f in $A;
do
    echo "Processing: $f"
    cat $f | sed s/PyQt4/PyQt5/g > $T
    mv $T $f
done
