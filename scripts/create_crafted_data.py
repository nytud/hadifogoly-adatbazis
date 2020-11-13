"""
Create one crafted data record to test how the transcription works.
Each data field value can be specified via CLI arguments.
"""

import argparse
import sys


SOURCE_FILE = 'data/data.header.csv'

OPTIONS = [
    ['l', 'family-name', 'set family name', 2],
    ['f', 'christian-name', 'set christian name', 3],
    ['F', 'father-name', 'set father\'s christian name', 4],
    ['H', 'home-address', 'set home address', 6],
    ['C', 'place-of-capture', 'set place-of-capture', 7]
]
# indices
SHORT = 0
LONG = 1
HELP = 2
INDEX = 3 # from 1! (as `cut` does)


def main():
    """Main."""
    # get CLI arguments
    args = get_args()
    # ... as a dict!
    args_dict = vars(args)

    with open(SOURCE_FILE, 'r') as fh:
        record = fh.readline().strip() # SOURCE_FILE's 1st record considered

    # mark original field values which are not changed
    fields = [f'#{field}#' for field in record.split('\t')]

    for option in OPTIONS:
        arg_value = args_dict[option[LONG].replace('-', '_')]
        if arg_value is not None:
            fields[option[INDEX] - 1] = arg_value
            # -1 => convert indices from 1 to indices from 0

    print('\t'.join(fields))


def get_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    for option in OPTIONS:
        parser.add_argument(
            f'-{option[SHORT]}',
            f'--{option[LONG]}',
            f'-{option[INDEX]}',
            help=f'{option[HELP]} = column #{option[INDEX]}',
            type=str
        )
        
    return parser.parse_args()


if __name__ == '__main__':
    main()
