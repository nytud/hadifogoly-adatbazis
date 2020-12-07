# -*- coding: utf-8 -*-
"""
This module contains some preprocessing to be done before extract_location_parts.
"""

import csv
import re
import sys


COUNTRY_NAME_ABBREVS = {
    'Авст.': 'Австрия',
    'Австр.': 'Австрия',
    'Австрии': 'Австрия',
    'Венг.': 'Венгрия',
    'Венгр.': 'Венгрия',
    'Венгрии': 'Венгрия',
    'Венгрия.': 'Венгрия',
    'Унгария': 'Венгрия',
    'Чех.': 'Чехословакия',
    'Чехосл.': 'Чехословакия',
    'Чехослов.': 'Чехословакия',
    'Чехословак.': 'Чехословакия',
    'Чехословакии': 'Чехословакия',
    'Ч.-Словакия': 'Чехословакия',
    'Словакии': 'Словакия',
    'Словак.': 'Словакия',
    'Германии': 'Германия',
    'Рум.': 'Румыния',
    'Румын.': 'Румыния',
    'Румынии': 'Румыния',
    'Югослав.': 'Югославия',
    'Югославии': 'Югославия',
    'Транс.': 'Трансильвания',
    'Трансильв.': 'Трансильвания',
    'Трансильван.': 'Трансильвания',
    'Укр.': 'Украина'
# Польша
}


def process():
    """Do the thing."""

    reader = csv.reader(sys.stdin, delimiter='\t')
    writer = csv.writer(sys.stdout, delimiter='\t')

    for row in reader:
        to_print = []
        for col, val in enumerate(row):

            # col: 0-tól számozva!

            # handle country name abbreviations
            if col in {5, 6}:
                for abbrev, fullform in COUNTRY_NAME_ABBREVS.items():
                    val = val.replace(abbrev, fullform)

            to_print.append(val)

        print('\t'.join(to_print))

def main():
    """Main."""
    process()

if __name__ == '__main__':
    main()
