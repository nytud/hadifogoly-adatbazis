"""
Generate city list using geonames database.
"""

import argparse
import sys

from coords import load_geonames_data


def main():
    """Main."""
    for cityname in load_geonames_data().keys():
        print(cityname)


if __name__ == '__main__':
    main()
