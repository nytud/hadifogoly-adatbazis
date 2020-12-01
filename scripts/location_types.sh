#!/bin/bash

cat data/Kart.csv | cut -d '	' -f 6 | sed "s/,/ ,/g;s/ /\t\t/g;s/^/\t/;s/$/\t/;s/\t[а-яА-Я][а-яА-Я]*\t/\tw\t/g;s/[0-9][0-9]*/#/g;s/\t\t/ /g;s/^\t//;s/\t$//;s/\. w/.=w/g;s/\. #/.=#/g;s/№ #/№=#/g;s/р-н w/р-н=w/g" | sort | uniq -c | sort -nr

