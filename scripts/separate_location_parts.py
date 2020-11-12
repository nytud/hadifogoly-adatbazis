# -*- coding: utf-8 -*-
"""
This module separates location parts
(country, county, city etc.)
to different columns (fields).
"""

import csv
import sys

from extract_location_parts import extract_location_parts as elp


LOCATION_FIELDS = [
    'country', 'county',
    'district', 'city', 'village',
    'street', 'number' ]

def process():
    """Do the thing"""

    reader = csv.reader(sys.stdin, delimiter='\t')
    writer = csv.writer(sys.stdout, delimiter='\t')

    for row in reader:
        new_col_number = 1
        to_print = []
        for col, val in enumerate(row):
            if col in {5, 6}: # 0-tól számozva!
                for location_field in LOCATION_FIELDS:
                    new_val = "{}".format(elp(val)[location_field])
                    to_print.append(new_val)
                    new_col_number += 1
            else:
                to_print.append(val)
                new_col_number += 1
        print('\t'.join(to_print))

def main():
    """Main."""
    process()

if __name__ == '__main__':
    main()
