#!/bin/sh

A=`find . -name "*.py"`

T="tmpfile"
for f in $A;
do
    echo -n "."
    cat $f | sed s/Noctopus/Sysmo/g > $T
    mv $T $f
done
