# -*- coding: utf-8 -*-
"""
This module contains some preprocessing to be done before transcription.
"""

import csv
import re
import sys

SAR_TABLE_FILENAME = 'data/sar_table.csv' # search-and-replace table
#SAR_MARK = '/R' # search-and-replace mark -- see in file

def process():
    """Do the thing."""

    search_and_replace = {}
    with open(SAR_TABLE_FILENAME) as csvfile:
        sar_reader = csv.reader(csvfile, delimiter='\t')
        for cnt, orig, transcribed in sar_reader:
            search_and_replace[orig] = transcribed

    reader = csv.reader(sys.stdin, delimiter='\t')
    writer = csv.writer(sys.stdout, delimiter='\t')

    for row in reader:
        to_print = []
        for col, val in enumerate(row):

            # col: 0-tól számozva!

            # remove closing (?) dot from firstnames + fathernames #13
            if col in {2, 3}:
                val = re.sub('\.', '', val)

            # remove closing dot from lastnames if not containing space #13
            if col in {1} and not ' ' in val:
                val = re.sub('\.$', '', val)

            # remove -вич/-вна endings from fathernames #12
            if col in {3}:
                val = re.sub('[ое]вич$', '', val)
                val = re.sub('[ое]вна$', '', val)

            # search-and-replace in firstnames + fathernames #11
            if col in {2, 3}:
                if val in search_and_replace:
                    val = search_and_replace[val]

            to_print.append(val)

        print('\t'.join(to_print))

def main():
    """Main."""
    process()

if __name__ == '__main__':
    main()
