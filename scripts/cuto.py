"""
A somewhat improved version of the `cut` command
for rearranging columns of a csv file.
Column reordering and column repeat are allowed.
Column spec can be something like: "2,1" or "4-6,2,8,8".
Columns counted from one. Zero means adding an empty column.
"""

import argparse
import sys


# XXX completely no error handling yet :)
def parse_column_spec(column_spec_string):
    """
    Parse column spec.
    "8-" format is not implemented,
    because it would require knowing length of csv rows.
    """

    intervals = column_spec_string.split(',')
    indices = []
    for interval in intervals:
        limits = interval.split('-')
        # 1 becomes 1-1 <--> 1-4 remains 1-4
        if len(limits) == 1: beg = end = limits[0]
        if len(limits) == 2: beg, end = limits
        indices.extend(
            list(range(int(beg), int(end) + 1)))

    return indices


def main():
    """Main."""
    args = get_args()

    cols = parse_column_spec(args.column_spec)

    for line in sys.stdin:
        row = line.strip().split('\t')
        out_row = []
        for col in cols:
            out_row.append(row[col-1] if col > 0 else '')
        print('\t'.join(out_row))


def get_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        '-c', '--column-spec',
        help='specify columns to choose, e.g. "2,1" or "4-6,2,8,8"',
        type=str,
        required=True
    )

    return parser.parse_args()


if __name__ == '__main__':
    main()
