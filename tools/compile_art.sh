#!/bin/bash

SFILE=SConstruct
WORK=/tmp/work

if [ $# -eq 2 ]
then
    ALIAS=$1
    LOCATION=$2
    if [ -f $SFILE ]
    then
        touch $WORK
        while [ -f $WORK ]
        do
            time make COLUMNS=$COLUMNS SELECTED="$ALIAS"; red_green_bar.py $? $COLUMNS
            echo -n 
            inotifywait ../${LOCATION}/text.md
        done
    else
        echo Nie jestem we wlasciwym katalogu, bo tu brak pliku: $SFILE
    fi
else
    echo Podaj linie z pliku z artykulami jako parametry:
    echo 1. alias
    echo 2. sciezka do artykulu
    echo np.:
    echo $0 ros workshops/IPython_Robot_Prototyping
fi
