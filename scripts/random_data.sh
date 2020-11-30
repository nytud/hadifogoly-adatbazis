#!/bin/bash

# random_1000.csv = random adat készítése
# $2 db random sor kiválasztása a rendes adatból

if [ $# -ne 3 ]
then
  echo
  echo "Exactly 3 param mandatory:"
  echo "  * infile = a tsv"
  echo "  * size = sample size"
  echo "  * seed = random seed for reproducibility"
  echo
  exit 1;
fi

INFILE=$1
SIZE=$2
SEED=$3

S=scripts

cat $INFILE | shuf -n $SIZE --random-source=<($S/get_seeded_random.sh $SEED) | sort -t '	' -k 1,1 -n

