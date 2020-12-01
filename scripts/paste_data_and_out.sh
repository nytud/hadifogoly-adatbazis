#!/bin/bash

DATAFILE=data/$1.csv
OUTFILE=out/$1.transcribed.csv

if [ $# -eq 2 ]
then
    COLS=$2
else
    if [ "$1" == "Kart_1000_Sor" ] # <- khm.. 2 oszloppal rövidebb..
    then
        COLS="1,2-4,6,7,19-21,23-27,30-34" # utca/házszám nélkül
        #COLS="1,2-4,19-21" # csak nevek
    else
        COLS="1,2-4,6,7,21-23,25-29,32-36" # utca/házszám nélkül
        #COLS="1,2-4,21-23" # csak nevek
    fi
fi

paste $DATAFILE $OUTFILE | cols $COLS

