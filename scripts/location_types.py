"""
Collect location description types.
"""

import argparse
import re
import sys


def main():
    """Process by line to represent location description type."""
    # get CLI arguments
    args = get_args()
    # ... as a dict!
    args_dict = vars(args)

    for line in sys.stdin:
        loc, other_loc = line.split('\t')[5:7]
        loc = loc.replace(',', '')
        loc = ' ' + loc.replace(' ', '  ') + ' '
        loc = re.sub(r' [ёа-яА-Я]+ ', ' w ', loc)
        loc = re.sub(r'[0-9]+', '#', loc)
        loc = loc.replace('  ', ' ')
        loc = loc.replace('. w', '.=w')
        loc = loc.replace('. #', '.=#')
        loc = loc.replace('№ #', '№=#')
        loc = loc.replace('р-н w', 'р-н=w')
        if args.sort:
            loc = ' '.join(sorted(loc.split(' ')))
        print(loc) # XXX van other_loc is! :)


def get_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        '-s', '--sort',
        help='sort tokens in line',
        action='store_true'
    )
    return parser.parse_args()


if __name__ == '__main__':
    main()
