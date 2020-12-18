"""
Get completes lines from _T_kesz*csv files.
"""

import argparse
import sys


def main():
    """Main."""

    # stdin -> stdout
    for line in sys.stdin:
        fields = line.strip().split('\t')
        if len(fields) > 3 and fields[3]:
            print('\t'.join([fields[0], fields[1], fields[3] + '/R']))


if __name__ == '__main__':
    main()
