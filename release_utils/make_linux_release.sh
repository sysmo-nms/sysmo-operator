#!/bin/sh

OUTPUT="linux_rel"
rm -rf $OUTPUT
mkdir $OUTPUT

for lib in $(objdump -p sysmo-operator | grep NEEDED | awk '{print $2}')
do
  LIB_LINE=$(ldconfig -p | grep $lib)
  LN_DEST=$(echo $LIB_LINE | awk '{print $NF'})
  cp -L $LN_DEST $OUTPUT/
done

cp release_utils/sysmo-operator.sh $OUTPUT/
chmod +x $OUTPUT/sysmo-operator.sh

cp sysmo-operator $OUTPUT/
