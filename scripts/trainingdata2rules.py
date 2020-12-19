"""
Process training data. Generate rules.
"""

import argparse
import sys

from collections import defaultdict


rules = defaultdict(lambda: defaultdict(int)) # :)


def main():
    """Main."""

    # stdin -> stdout identity filter
    for line in sys.stdin:
        fields = line.strip().split('\t')
        if len(fields) < 4:
            continue
        orig, trans = fields[2:4]

        if not ' ' in orig:
          orig = [ch for ch in orig]
        else:
          orig = orig.split(' ')
        if not ' ' in trans:
          trans = [ch for ch in trans]
        else:
          trans = trans.split(' ')

        # XXX ha el akarjuk különíteni a szó elejét és végét
        #orig[0] = '^' + orig[0]
        #orig[-1] = orig[-1] + '$'
        #trans[0] = '^' + trans[0]
        #trans[-1] = trans[-1] + '$'

        for a, b in zip(orig, trans): # :)
            rules[a][b] += 1

    # print result with percentages
    for orig_char, trans_chars in sorted(rules.items()):
        summa = sum(trans_chars.values())
        print(orig_char, '->', summa,
            [f'{trans_char} {val/summa:.1%}({val})'
            for trans_char, val in
            sorted(trans_chars.items(),
                key=lambda item: item[1],
                reverse=True)])


if __name__ == '__main__':
    main()
