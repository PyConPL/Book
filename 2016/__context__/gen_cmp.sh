#!/bin/bash

EXP_DIR=expected
if [ ! -e $EXP_DIR ]
then
    echo Creating the directory '"'$EXP_DIR'"'.
    mkdir $EXP_DIR
fi

if [ -d $EXP_DIR ]
then
    (cd build; tar cf - `find . -name \*.tex`) | (cd $EXP_DIR; tar -xvf -)
else
    echo Wrong type of '"'$EXP_DIR'"' - it should be a directory:
    ls -ld $EXP_DIR
fi
