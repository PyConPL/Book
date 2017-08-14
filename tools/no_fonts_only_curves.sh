#!/bin/bash
# gs version >= 9.15
if [ $# -eq 1 ]
then
    SRC=$1
    if [ -f $SRC ]
    then
        TMP=gen_tmp_file.pdf
        if gs -dNoOutputFonts -sDEVICE=pdfwrite -o $TMP $SRC
        then
            mv $TMP $SRC
        else
            echo Ghostscript failed.
        fi
    else
        echo No such file: $SRC
        ls -l $SRC
    fi
else
    echo Specify PDF file name.
fi
