#!/bin/bash

# 2020.12.15. @b7394d9 alapján készült
paste data/random_10000_42.preprocessed.csv out/random_10000_42.transcribed.new.csv > tmp.$$

OUTDIR=data/sar_tables

# lastname.csv 2
cat tmp.$$ | cols "2,33" | grep =T | sstat | sed "s/^  *//;s/ /	/" > $OUTDIR/lastname_T.csv

# firstname.csv 3,4
( cat tmp.$$ | cols "3,34" ; cat tmp.$$ | cols "4,35" ) | grep =T | sstat | sed "s/^  *//;s/ /	/" > $OUTDIR/firstname_T.csv

# county.csv 7,14
( cat tmp.$$ | cols "7,38" ; cat tmp.$$ | cols "14,45" ) | grep =T | sstat | sed "s/^  *//;s/ /	/" > $OUTDIR/county_T.csv

# city.csv 9,16
( cat tmp.$$ | cols "9,40" ; cat tmp.$$ | cols "16,47" ) | grep =T | sstat | sed "s/^  *//;s/ /	/" > $OUTDIR/city_T.csv

rm -f tmp.$$

