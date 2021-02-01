#!/bin/bash

DEFAULT_DATAFILE=Kart

DEFAULT_CHUNKS=2400 # can be divided by 2, 3, 4, 6, 24...

if [ $# -eq 0 ]
then
  DATAFILE=$DEFAULT_DATAFILE
  CHUNKS=$DEFAULT_CHUNKS
  FROM=0
  TO=$((CHUNKS - 1))
elif [ $# -eq 2 ]
then
  DATAFILE=$1
  CHUNKS=$2
  FROM=0
  TO=$((CHUNKS - 1))
elif [ $# -eq 4 ]
then
  DATAFILE=$1
  CHUNKS=$2
  FROM=$3
  TO=$4
else
  echo "zero or 2 (DATAFILE and CHUNKS) or 4 (+ FROM and TO) parameter needed"
  exit 1
fi

INPUT=data/$DATAFILE.csv

OUTDIR=$DATAFILE.splits
rm -rf $OUTDIR
mkdir -p $OUTDIR


# !!! number of cores !!!
# https://stackoverflow.com/questions/6481005
CORES=$(grep -c ^processor /proc/cpuinfo)
echo "# of cores = $CORES"

SUFFIX_LENGTH=4
PREFIX=$OUTDIR/$DATAFILE.c
ADD_SUFFIX=.csv
CHUNKS_FILES_PATTERN="$PREFIX????$ADD_SUFFIX" # according to $PREFIX and $SUFFIX_LENGTH
echo $CHUNKS_FILES_PATTERN

echo "--- split $FROM..$TO"
split --number l/$CHUNKS --numeric-suffixes --suffix-length=$SUFFIX_LENGTH --additional-suffix=$ADD_SUFFIX $INPUT $PREFIX

for i in $(seq -f "%04g" 0 $(($FROM - 1)))
do
  echo "rm -f $PREFIX$i$ADD_SUFFIX"
  rm -f $PREFIX$i$ADD_SUFFIX
done
for i in $(seq -f "%04g" $(($TO + 1)) $(($CHUNKS - 1)))
do
  echo "rm -f $PREFIX$i$ADD_SUFFIX"
  rm -f $PREFIX$i$ADD_SUFFIX
done

LOCKFILE=/var/lock/mylockfile
NUMBER_OF_FILES=$(($TO-$FROM+1))

echo "--- run for $NUMBER_OF_FILES files"
for file in $CHUNKS_FILES_PATTERN ; do

    (
        # https://unix.stackexchange.com/questions/274498
        flock -n 9 || exit 1
        # commands executed under lock
        echo -n "$file "
        date
    ) 9>$LOCKFILE

    ((i=i%CORES)); ((i++==0)) && wait


    FILE_FOR_MAKE=$(echo $file | sed "s/$ADD_SUFFIX$//")
    make FILE=$FILE_FOR_MAKE DATADIR=. OUTDIR=. transcribe &
    # $file=split/c0000.csv
    # FILE=FILE_FOR_MAKE=split/c0000
    # DATADIR=.
    # OUTDIR=.
    #
    # azért '.' mert a $file tartalmazza a split könyvtárat,
    # ami az input és az output is egyben! :)

done

rm -f $LOCKFILE
