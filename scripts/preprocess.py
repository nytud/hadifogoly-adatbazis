# -*- coding: utf-8 -*-
"""
This module contains some preprocessing to be done before transcription.
"""

import csv
import re
import sys

# search-and-replace table
SAR_TABLE_DIR = 'data/sar_tables'
SAR_TABLE_COLUMNS = ['lastname', 'firstname', 'county', 'district', 'city']
#SAR_MARK = '/R' # search-and-replace mark -- see in file

PREPOSITIONS = [
    'в',  # -bAn
    'около',  # közel
    'на',  # -On -- ez talán mégis szükséges? "на Дону" hm.. XXX
    'под',  # alatt
    'близ', # mellett, közelében
    'близь', # ua.
    'вблизи', # ua.
    'возле', # ua.
    'у', # -nÁl
    'из', # -bÓl
]
# all preps are needed with two spaces and then with one space
# (because of the output of separate_location_parts.py)
PREPOSITIONS_WITH_SPACES = [f'{p}  ' for p in PREPOSITIONS] + [f'{p} ' for p in PREPOSITIONS]


def read_sar_table(filename):
    """Read a search and replace table."""
    sar = {}
    with open(filename) as csvfile:
        sar_reader = csv.reader(csvfile, delimiter='\t')
        for orig, transcribed, *_ in sar_reader:
            sar[orig] = transcribed
    return sar


def process():
    """Do the thing."""

    sar = {}
    for colname in SAR_TABLE_COLUMNS:
        sar[colname] = read_sar_table(f'{SAR_TABLE_DIR}/{colname}.csv')

    reader = csv.reader(sys.stdin, delimiter='\t')
    #writer = csv.writer(sys.stdout, delimiter='\t')

    for row in reader:
        to_print = []
        for col, val in enumerate(row):

            # col: 0-tól számozva!

            # remove closing dot from lastnames if not containing space #13
            if col in {1} and not ' ' in val:
                val = re.sub('\.$', '', val)

            # search-and-replace for lastnames
            if col in {1}:
                if val in sar['lastname']:
                    val = sar['lastname'][val]

            # remove closing (?) dot from firstnames + fathernames #13
            if col in {2, 3}:
                val = re.sub('\.', '', val)

            # remove -вич/-вна endings from fathernames #12
            if col in {3}:
                val = re.sub('[ое]вич$', '', val)
                val = re.sub('[ое]вна$', '', val)

            # search-and-replace for firstnames + fathernames #11
            if col in {2, 3}:
                if val in sar['firstname']:
                    val = sar['firstname'][val]

            # remove -ский/-ская endings from places
            if col in {5, 6, 7, 8, 12, 13, 14, 15}:
                val = re.sub('ский$', '', val)
                val = re.sub('ская$', '', val)

            # remove prepositions from places
            if col in {5, 6, 7, 8, 12, 13, 14, 15}:
                for pattern in PREPOSITIONS_WITH_SPACES:
                    val = re.sub(f'^{pattern}', '', val)

            # search-and-replace for counties
            if col in {6, 13}:
                if val in sar['county']:
                    val = sar['county'][val]

            # search-and-replace for districts
            if col in {7, 14}:
                if val in sar['district']:
                    val = sar['district'][val]

            # search-and-replace for cities
            if col in {8, 15}:
                if val in sar['city']:
                    val = sar['city'][val]

            to_print.append(val)

        print('\t'.join(to_print))

def main():
    """Main."""
    process()

if __name__ == '__main__':
    main()
