#!/bin/bash
NAMES=`cd expected;find * -type f -name \*.tex`
for i in $NAMES
do
    FILE=`basename $i .tex`
    LABEL=`basename $i`
    DST=src/$FILE.diff
    diff -ru -L $LABEL build/$i expected/$i > $DST
    echo $DST done.
done
