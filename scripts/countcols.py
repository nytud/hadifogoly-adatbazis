# -*- coding: utf-8 -*-
"""
This module simply counts columns of a tsv file line by line.
"""


import csv
import sys


def main():
    """Do the thing."""
    for row in csv.reader(sys.stdin, delimiter='\t'):
        print(len(row))


if __name__ == '__main__':
    main()
