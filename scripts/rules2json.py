# -*- coding: utf-8 -*-
"""Convert 'rules plain txt' format into strict/loose JSONs."""

import sys
from collections import OrderedDict


SEPARATOR = ' ' # separator between fields
OPTIONSEP = '|' # separator inside field #3
EPSILON = "''" # indicates: convert a letter to empty string

PRG = sys.argv[0]


def process(inputfile, outputfile, mode):
    """
    Process input as strict or as loose.
    mode can be 'strict' or 'loose'
    """

    mode = 'loose' if mode == 'loose' else 'strict'

    # 1. read

    with open(inputfile) as ifile:
        lines = [line.rstrip() for line in ifile]
    lines = [line
             for line in lines
             if line != '' and not line.startswith('#')]

    all_but_two_char = OrderedDict() # 1,3,4,5...-char source forms
    exactly_two_char = OrderedDict() # 2-char source forms
    # handled differently
    # = supplemented by all one-char+one-char possibilities
    #   i.e. 'ей' can be 'é', but also 'ej|ely|ei|éj|ély|éi|öj...'

    for i, line in enumerate(lines):
        fields = line.split(SEPARATOR)
        if len(fields) < 2 or len(fields) > 3:
            print(line)
            print("{} ERROR: no of fields (split by '{}') must be 2 or 3".format(PRG, SEPARATOR))
            exit(1)

        f0 = fields[0]
        f1 = fields[1]
        f2 = fields[2] if len(fields) == 3 else None
        # mindenképp 3 mező legyen :)

        # change EPSILON to empty string
        f1 = f1.replace(EPSILON, '')
        if f2 is not None:
            f2 = f2.replace(EPSILON, '')

        from_what = f0
        if mode == 'strict':
            to_what = [ f1 ]
        else: # 'loose'
            if f2 is not None:
                to_what = [ f1 ] + f2.split(OPTIONSEP)
            else:
                to_what = [ f1 ]

        if len(from_what) == 1:
            all_but_two_char[from_what] = to_what
        # csak loose esetén vesszük a 2-char from_what ptn-ket!
        elif len(from_what) == 2:
            if mode == 'loose':
                exactly_two_char[from_what] = to_what
            # itt alább direkt van ua, ti. az a nagy szám,
            # hogy a kétkaraktereseknél strict-nél
            # az egyben definiált megfelelőt vesszük! XXX XXX
            # -- de nem egyértelmű, hogy segít
            #    az alább kommentben részletezettek miatt!
            else: # 'strict'
                exactly_two_char[from_what] = to_what
        else:
            all_but_two_char[from_what] = to_what
            #print(line)
            #print("{} ERROR: 'from_what' can be 1 or 2 chars long".format(PRG))
            #exit(1)

    # 2. extend 2-char ptns with 1-char options

    # csak loose esetén vesszük a 2-char from_what ptn-ket!
    # strict esetén marad a 2 char megfelelője külön-külön.
    # akkor lehetne strict-ben is figyelembe venni őket,
    # ha azt lehetne mondani,
    # hogy az adott két betűnek, ha egymás mellett vannak,
    # akkor az együttes átírása az elsődleges
    # -- de ezt most nem lehet mondani! XXX :)
    #
    # XXX XXX XXX lehetne esetleg így:
    # ей é . => strictnél: é az elsődleges, és nem külön a kettő
    # ей . é => strictnél: a két betű külön-külön az elsődleges
    # (loose esetén ua a kettő)
    # -- ez elég bonyolultnak tűnik, egyelőre tutira hagyom! :)
    #
    #if mode == 'strict':
    #    for ptn in exactly_two_char:
    #        exactly_two_char[ptn] = [ 
    #            all_but_two_char[ptn[0]][0] + all_but_two_char[ptn[1]][0] ]

    # 2-char ptn extension @ loose
    if mode == 'loose':
        for ptn in exactly_two_char:
            acc = []
            for i in all_but_two_char[ptn[0]]:
                for j in all_but_two_char[ptn[1]]:
                    acc.append(i + j)
            acc += exactly_two_char[ptn]
            exactly_two_char[ptn] = acc

    # 3. write

    with open(outputfile, 'w') as ofile:

        # concat...
        patterns = all_but_two_char
        patterns.update(exactly_two_char)

        print('{', file=ofile)

        for i, from_what in enumerate(patterns):
            to_what = patterns[from_what]

            if len(to_what) == 1:
                to_what = to_what[0]
            else:
                to_what = '(' + '|'.join(to_what) + ')'

            print('    "{}": "{}"'.format(from_what, to_what), end='', file=ofile)
            print(',' if i < len(patterns) - 1 else '', file=ofile)

        print('}', file=ofile)


def main():
    """Main."""

    inputfile = sys.argv[1] + '.rules'
    output_strict = sys.argv[1] + '_strict.json'
    output_loose = sys.argv[1] + '_loose.json'

    process(inputfile, output_strict, 'strict')
    process(inputfile, output_loose, 'loose')

if __name__ == '__main__':
    main()
