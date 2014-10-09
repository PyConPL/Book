#!/bin/bash
NAMES=`cd expected;find * -type f -name \*.tex`
for i in $NAMES
do
    FILE=`basename $i .tex`
    DST=src/$FILE.diff
    diff -ru build/$i expected/$i > $DST
    echo $DST done.
done
