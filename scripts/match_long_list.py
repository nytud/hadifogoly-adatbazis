# -*- coding: utf-8 -*-
"""Matches regexes in argv[2] to list of terms in argv[1]."""

import sys
import re

def read_list(filename):
    """Read list for regex match."""
    with open(filename) as listfile:
        alist = listfile.read().splitlines()
    return alist

def main():
    """Main."""
    termlist = read_list(sys.argv[1])
    regexlist = read_list(sys.argv[2])
    for regex in regexlist:
        compiled_regex = re.compile(regex)
        matches = list(filter(compiled_regex.fullmatch, termlist))
        print(regex, end=' ')
        print(len(matches), end=' ')
        print(matches[0:5])

if __name__ == '__main__':
    main()
