#!/bin/bash

FILE=random_10000_42

cat data/$FILE.csv | cols 6 > a
cat out/$FILE.transcribed.new.csv | cols 9 > b
cat out/$FILE.transcribed.new_fullgeonames.csv | cols 9 > c
paste a b c | awk -F '	' '{ if ( $2 != $3) { printf "%s\t%s\t%s\n", $1, $2, $3 } }' | sstat | sstat2tsv > geonames_test.6.csv

cat data/$FILE.csv | cols 7 > a
cat out/$FILE.transcribed.new.csv | cols 16 > b
cat out/$FILE.transcribed.new_fullgeonames.csv | cols 16 > c
paste a b c | awk -F '	' '{ if ( $2 != $3) { printf "%s\t%s\t%s\n", $1, $2, $3 } }' | sstat | sstat2tsv > geonames_test.7.csv

rm -f a b c

