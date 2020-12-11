#!/bin/bash

# el lehetett volna indulni a git clone-ból,
# és abból törölgetni... 

# deploy directory
D=$1

rm -rf $D

mkdir $D
mkdir $D/data
mkdir $D/rules
mkdir $D/scripts
mkdir $D/out

cp -p README.md $D
cp -p README.pdf $D
cp -p Makefile $D

# data
# vvv LÉNYEG!
cp -rp data/lists $D/data
cp -p data/Kart.csv $D/data
cp -p data/Kart_1000_Sor.csv $D/data
cp -p data/test_set.csv $D/data
cp -p data/pseudo_1000_42.csv $D/data
cp -p data/random_10000_42.csv $D/data
cp -p data/data.header.csv $D/data
cp -p data/data.header.new.csv $D/data
cp -rp data/sar_tables $D/data
#
# *preprocessed* nem kell
# data/Kart.preprocessed.csv <- az az, ami nincs!
# cp -p data/Kart_1000_Sor.preprocessed.csv $D/data
# cp -p data/test_set.preprocessed.csv $D/data

# rules
cp -p rules/metarules.txt $D/rules
cp -p rules/metarules.json $D/rules
cp -p rules/nat_loose.json $D/rules
cp -p rules/nat.rules $D/rules
cp -p rules/nat_strict.json $D/rules
cp -p rules/ru2de_loose.json $D/rules
cp -p rules/ru2de.rules $D/rules
cp -p rules/ru2de_strict.json $D/rules
cp -p rules/ru2hu_loose.json $D/rules
cp -p rules/ru2hu.rules $D/rules
cp -p rules/ru2hu_strict.json $D/rules

# scripts
cp -p scripts/difflib_ratio_test.py $D/scripts
cp -p scripts/difflib_test.py $D/scripts
cp -p scripts/eval.sh $D/scripts
cp -p scripts/extract_location_parts.py $D/scripts
cp -p scripts/metarules2json.py $D/scripts
cp -p scripts/omit_parenth_names.py $D/scripts
cp -p scripts/preextract.py $D/scripts
cp -p scripts/preprocess.py $D/scripts
cp -p scripts/ru2hu.py $D/scripts
cp -p scripts/rules2json.py $D/scripts
cp -p scripts/separate_location_parts.py $D/scripts
cp -p scripts/simply_transcript_text.py $D/scripts
cp -p scripts/split_and_parallel.sh $D/scripts
cp -p scripts/transcribe.py $D/scripts

# out
# vvv LÉNYEG!
cp -p out/Kart.transcribed.csv $D/out
cp -p out/Kart.eval.out $D/out
cp -p out/Kart.eval_by_col.out $D/out
cp -p out/Kart_1000_Sor.transcribed.csv $D/out
cp -p out/Kart_1000_Sor.eval.out $D/out
cp -p out/Kart_1000_Sor.eval_by_col.out $D/out
cp -p out/test_set.transcribed.csv $D/out
cp -p out/test_set.eval.out $D/out
cp -p out/test_set.eval_by_col.out $D/out
cp -p out/pseudo_1000_42.transcribed.csv $D/out
cp -p out/pseudo_1000_42.eval.out $D/out
cp -p out/pseudo_1000_42.eval_by_col.out $D/out
cp -p out/random_10000_42.transcribed.csv $D/out
cp -p out/random_10000_42.eval.out $D/out
cp -p out/random_10000_42.eval_by_col.out $D/out
cp -p out/noi_nevek_eval.txt $D/out

