# -*- coding: utf-8 -*-
"""
This module contains some preprocessing to be done before extract_location_parts.
"""

import csv
import re
import sys


# XXX hardcoded
COUNTRY_NAME_ABBREVS_FILE = 'data/prelists/orszagok_ru_rovidites.csv'
COUNTRY_NAME_ABBREVS = {}


def process():
    """Do the thing."""

    with open(COUNTRY_NAME_ABBREVS_FILE, encoding='utf-8') as abbrevs:
        for row in csv.reader(abbrevs, delimiter='\t'):
            full, abbr = row[:2]
            if full != abbr:
                COUNTRY_NAME_ABBREVS[abbr] = full

    for row in csv.reader(sys.stdin, delimiter='\t'):
        to_print = []
        for col, val in enumerate(row):

            # col: 0-tól számozva!

            # handle country name abbreviations
            if col in {5, 6}:
                tokens = re.split('([ ,])', val) # jó lesz, vö: extract_location_parts.py / split
                converted = [COUNTRY_NAME_ABBREVS[token] if token in COUNTRY_NAME_ABBREVS else token for token in tokens]
                val = ''.join(converted)

            to_print.append(val)

        print('\t'.join(to_print))

def main():
    """Main."""
    process()

if __name__ == '__main__':
    main()
