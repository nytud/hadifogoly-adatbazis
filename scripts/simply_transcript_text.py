# -*- coding: utf-8 -*-
"""This is a simple ru2hu.Transcriptor() test."""

import json
import sys

from ru2hu import Transcriptor


def test():
    """Do the thing."""
    filename = sys.argv[1]
    with open(filename) as config:
        table = json.load(config)

    trans = Transcriptor(table)

    text = sys.argv[2]

    print(text)
    print(trans(text))

def main():
    """Main."""
    test()

if __name__ == '__main__':
    main()

