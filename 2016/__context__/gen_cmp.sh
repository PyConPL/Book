#!/bin/bash

EXP_DIR=expected
BUILD_DIR=build
if [ ! -e $EXP_DIR ]
then
    echo Creating the directory '"'$EXP_DIR'"'.
    mkdir $EXP_DIR
fi

if [ -d $EXP_DIR ]
then
    if [ -d $BUILD_DIR ]
    then
        (cd $BUILD_DIR; tar cf - `find . -name \*.tex`) | (cd $EXP_DIR; tar -xvf -)
    else
        echo Wrong type of '"'$BUILD_DIR'"' - it should be a directory:
        ls -ld $BUILD_DIR
        echo Maybe you should generate it using:
        echo 'time make COLUMNS=$COLUMNS'
    fi
else
    echo Wrong type of '"'$EXP_DIR'"' - it should be a directory:
    ls -ld $EXP_DIR
fi
