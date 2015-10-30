#!/bin/sh
APPNAME=`basename $0 | sed s/\.sh$//`
DIRNAME=`dirname $0`
tmp="${dirname#?}"

if [ "${dirname%$tmp}" != "/" ]; then
    DIRNAME=$PWD/$DIRNAME
fi

LD_LIBRARY_PATH=$DIRNAME
export LD_LIBRARY_PATH

ldd $DIRNAME/$APPNAME

# see "lsof -P -T -p PID" to see runtime libraries
# see "ldd APP"
# see "objdump -p APP" | grep NEEDE
# see wikipedia rpath

# problem with LD_LIBRARY_PATH, it is used if no other
# default system library matchs.

$DIRNAME/$APPNAME "$@"
