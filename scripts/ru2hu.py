#! /usr/bin/env python3

"""Raw transcription tool from Russian to Hungarian.

Read TSV data from STDIN, write to STDOUT.
"""

import argparse
import csv
import json
import re
import sys


MINCOLS = 12
# columns to be transcript -- numbers < MINCOLS are safe :)
COLS = [1, 2, 3, 5, 6]


def get_args():
    """Handling of commandline arguments.
    """
    pars = argparse.ArgumentParser(description=__doc__)
    pars.add_argument(
        '-c',
        '--config',
        help='Path to JSON file containg transcription table.',
    )
    args = vars(pars.parse_args())
    return args


class Transcriptor:
    """Szótár (mit --> mire) alapján átír egy stringet egy másikra.

    Megvalósítás: a str.translate gyors, de csak 1-1-ben tudja a karaktereket
    párosítani. A hosszabb substring-substring cseréket a str.replace()-el
    cseréljük. Ahol számít a kontextus is, ott muszáj regex-eket használni. A
    sorrend fordított: először lecseréljük a kontextusos substringeket, amíg
    megvan a kontextus, utána cseréljük a többit (itt már nem számít a
    sorrend).
    """

    def __init__(self, table):
        self.translate_table = str.maketrans(
            {k: v for k, v in table.items() if len(k) == 1 and len(v) == 1})
        self.replace_table = \
            {k: v for k, v in table.items() if len(k) == 1 and len(v) != 1}
        self.regex_table = \
            {re.compile(k): v for k, v in table.items() if len(k) > 1}

    def __call__(self, text):
        for k, v in self.regex_table.items():
            text = k.sub(v, text)
        for k, v in self.replace_table.items():
            text = text.replace(k, v)
        text = text.translate(self.translate_table)
        return text


def main(config):
    with open(config) as config:
        table = json.load(config)
    tr = Transcriptor(table)
    reader = csv.reader(sys.stdin, delimiter='\t')
    writer = csv.writer(sys.stdout, delimiter='\t')
    for row in reader:
        # sanity check
        if len(row) < MINCOLS:
            print(f'wrong row. at least {MINCOLS} fields needed. {len(row)} available:\n\t{row}', file=sys.stderr)
            continue
        # transcript columns
        for col in COLS:
            row[col] = tr(row[col])
        writer.writerow(row)


if __name__ == '__main__':
    args = get_args()
    main(**args)
