#!/bin/sh
APPNAME=`basename $0 | sed s/\.sh$//`
DIRNAME=`dirname $0`
tmp="${dirname#?}"

if [ "${dirname%$tmp}" != "/" ]; then
    DIRNAME=$PWD/$DIRNAME
fi

LD_LIBRARY_PATH=$DIRNAME
export LD_LIBRARY_PATH

$DIRNAME/$APPNAME "$@"
