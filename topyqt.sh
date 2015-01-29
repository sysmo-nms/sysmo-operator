#!/bin/sh

A=`find . -name "*.py"`

T="tmpfile"
for f in $A;
do
    cat $f | sed s/PySide/PyQt4/g | sed s/Signal/pyqtSignal/g > $T
    mv $T $f
done
