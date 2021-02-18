# -*- coding: utf-8 -*-
"""
Omit the original name if there is a parenthesized version instead.
"""

import csv
import re
import sys

def process():
    """Do the thing."""

    reader = csv.reader(sys.stdin, delimiter='\t')
    writer = csv.writer(sys.stdout, delimiter='\t')

    for row in reader:
        to_print = []
        for col, val in enumerate(row):
            if col in {1, 2, 3}: # 0-tól számozva!
                #val = re.sub(' \(.*\)', '', val)
                val = re.sub(r'^.+ \((.+)\)$', r'\1', val)
                val = re.sub('см. ', '', val)
            to_print.append(val)
        print('\t'.join(to_print))

def main():
    """Main."""
    process()

if __name__ == '__main__':
    main()
