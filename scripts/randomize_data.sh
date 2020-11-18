#!/bin/bash

# pseudo_1000.csv = pszeudoadat készítése
# oszlopcsoportok egymástól független randomizálásával
# 
# pl. 3,4,13 = keresztnév + apai keresztnév + rangfokozat
# egyben marad (azonos seed-del randomizáltati!),
# mert pl. a női neveknél összefügg! Erre figyelni kell!


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


ACTSEED=$SEED
cat $INFILE | cut -d '	' -f 2     | shuf -n $SIZE --random-source=<($S/get_seeded_random.sh $ACTSEED) > b

ACTSEED=$((SEED+1))
cat $INFILE | cut -d '	' -f 3,4   | shuf -n $SIZE --random-source=<($S/get_seeded_random.sh $ACTSEED) > c

ACTSEED=$((SEED+2))
cat $INFILE | cut -d '	' -f 5     | shuf -n $SIZE --random-source=<($S/get_seeded_random.sh $ACTSEED) > d

ACTSEED=$((SEED+3))
cat $INFILE | cut -d '	' -f 6     | shuf -n $SIZE --random-source=<($S/get_seeded_random.sh $ACTSEED) > e

ACTSEED=$((SEED+4))
cat $INFILE | cut -d '	' -f 7     | shuf -n $SIZE --random-source=<($S/get_seeded_random.sh $ACTSEED) > f

ACTSEED=$((SEED+5))
cat $INFILE | cut -d '	' -f 8-12  | shuf -n $SIZE --random-source=<($S/get_seeded_random.sh $ACTSEED) > g

# XXX ez a lényeg, hogy itt SEED+1 van, hogy 3,4,13 egyben legyen!
ACTSEED=$((SEED+1))
cat $INFILE | cut -d '	' -f 13    | shuf -n $SIZE --random-source=<($S/get_seeded_random.sh $ACTSEED) > h

ACTSEED=$((SEED+6))
cat $INFILE | cut -d '	' -f 14-19 | shuf -n $SIZE --random-source=<($S/get_seeded_random.sh $ACTSEED) > i


# sorszám az elejére 2000000-tól
START=2000000
for ((i=START+1;i<=START+SIZE;i++))
do
  echo $i
done > a

paste a b c d e f g h i

rm -f a b c d e f g h i

