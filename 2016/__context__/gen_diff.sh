#!/bin/bash
NAMES=`cd expected;find * -type f -name \*.tex`
for i in $NAMES
do
    FILE=`basename $i .tex`
    LABEL=`basename $i`
    DST=src/$FILE.diff
    BUILD=build/$i
    if [ -f $BUILD ]
    then
        diff -ru -L $LABEL -L $LABEL $BUILD expected/$i > $DST
    else
        echo Skipped - no file: $BUILD
    fi
    echo $DST done.
done
