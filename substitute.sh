#!/bin/sh

A=`find . -name "*.py"`

T="tmpfile"
for f in $A;
do
    cat $f | sed s/opus\.monitor/monitor/g > $T
    mv $T $f
done
