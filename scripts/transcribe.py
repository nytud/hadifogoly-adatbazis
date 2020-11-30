# -*- coding: utf-8 -*-
"""
This module tries to identify
Hungarian version of NE-s (names, locations)
which are written in Cyrillic script
in the Hungarian Prisoner of War Database.
"""

# kiindulópont: ru2hu.py

import argparse
from collections import defaultdict
import csv
import difflib
import json
import re
import sys

from extract_location_parts import extract_location_parts as elp
from ru2hu import Transcriptor


# akarunk-e jelölést az alábbiak szerint
IS_MARK = True            # False if '-p'

# ha jelölni akarjuk, hogy mit találtunk meg a termlistán
AS_STRICT = '/S'          # 1. strict-ként megvan simán

AS_LOOSE = '/L'           # 2. loose-ként megvan

STRICT_FIRST_STEP = False
# akarunk-e difflib guess-t
IS_DIFFLIB = True         # False if '-n' 
DIFFLIB_CUTOFF = 0.8      # set by '-f'
AS_DIFFLIB = '/D'         # 3. difflib-ként megvan
FROM_STRICT = '>>'        # difflib esetén a strict alak jele

AS_FALLBACK = '=T'        # 4. ha nincs más, marad a strict

SAR_MARK = '/R'           # search-and-replace mark, see: preprocess.py


def build_one(data):
    """Initialize one set of transcriptor tools."""

# 1. előkészítjük a loose/strict Transciptorokat

    # XXX legyen portable...
    loose_filename = 'rules/' + data['loose'] + '.json'
    with open(loose_filename) as loose_config:
        loose_table = json.load(loose_config)
    data['loose_trans'] = Transcriptor(loose_table)

    # XXX legyen portable...
    strict_filename = 'rules/' + data['strict'] + '.json'
    with open(strict_filename) as strict_config:
        strict_table = json.load(strict_config)
    data['strict_trans'] = Transcriptor(strict_table)

# 2. előkészítjük a termlist segédlistát

    # XXX legyen portable...
    termlist_filename = 'data/lists/' + data['termlist'] + '.csv'
    with open(termlist_filename) as termlist:
        data['terms'] = [
            item.replace(' ', '_')
            for item
            in termlist.read().splitlines()]
        # set()-tel lassabb volt, pedig "5. pont"! hm..

# cache -- mezőnként!

    data['cache'] = defaultdict(str)

    return data


# XXX all data is in-memory!
# XXX persze lehetne egy osztály ez az izé...
def build_infrastructure(config):
    """Initialize all necessary data structures."""

    with open(config) as config:
        infrastructure = json.load(config)

    # XXX str JSON keys -> int python keys
    infrastructure = {int(k):v for k,v in infrastructure.items()}
    for col, data in infrastructure.items():

        data = build_one(data)

        # a fentit megcsináljuk a beágyazott 'strptn' izékre is
        # nem lehet ezt valahogy sokkal egyszerűbben? XXX
        if 'strptn' in data:
            # XXX str JSON keys -> int python keys -- ne legyen 2x!
            data['strptn'] = {int(k):v for k,v in data['strptn'].items()}
            for col_to_match, col_to_match_dict in data['strptn'].items():
                for strptn, strptn_dict in col_to_match_dict.items():
                    strptn_dict = build_one(strptn_dict)

    return infrastructure


def process(infrastructure):
    """Do the thing."""

    reader = csv.reader(sys.stdin, delimiter='\t')
    writer = csv.writer(sys.stdout, delimiter='\t')

    for row in reader:
        transcribed_row = row.copy()
        # kell az eredeti, mert hivatkozunk rá!

        # XXX ha row-ban nincs annyiadik col,
        #     ami viszont infrastructure-ban szerepel -> hibát kapunk!
        for col, data in infrastructure.items():

            # ha üres a mező, akkor passz
            if col >= len(row) or not row[col]:
                continue

# 3. vesszük adott mező adott adatát :)

            actual_data = data
            if 'strptn' in data:
                # most ez csak egy ilyen szabályt kezel!
                # XXX (esetleg valahogy tudna többet kezelni?)
                for col_to_match, col_to_match_dict in data['strptn'].items():
                    for strptn, strptn_dict in col_to_match_dict.items():
                        if row[col_to_match] == strptn:
                            actual_data = strptn_dict
                            break
            # vars()-sal lehet jobban? talán nem.
            loose_trans = actual_data['loose_trans']
            strict_trans = actual_data['strict_trans']
            terms = actual_data['terms']
            cache = actual_data['cache']

            # egyszerre csak 1 szót/elemet dolgozunk fel,
            # szóval nem kell a ciklus
            # (a dolgokat, pl. a helyeket, előre daraboljuk fel)
            one_word = row[col].replace(' ', '_')

            transcribed = ''

            # elnézést kérek az egytagú listán futtatott ciklusért
            # azért van, hogy használhassak continue-t :)
            # XXX hogy lehetne jobban (beágyazott if-ek nélkül)
            for word in [ one_word ]:

# legeslegelőszöris megnézzük, hogy a preprocessing.py feldolgozta-e

                if word.endswith(SAR_MARK):
                    transcribed = word
                    continue

# legelőszöris megnézzük a cache-ben

                if word in cache:
                    transcribed = cache[word]
                    continue

# 4. átírjuk strict (#5) szerint: trans = strict(name)

                trans = strict_trans(word)

# 5. ha így "egy-az-egyben" megvan a listán, akkor visszaadjuk
#    (amennyiben '-s' révén kértük ezt a lépést!)

                if STRICT_FIRST_STEP:
                    if trans in terms:
                        result = trans + AS_STRICT
                        transcribed = result
                        cache[word] = result
                        continue

# 6. átírjuk loose (#5) szerint: regex = loose(name)

                # itt jó a re.escape()!
                # mert a "loose" eredménye pont egy regex
                # a "(см." lezáratlan zárójelét oldja meg
                regex = loose_trans(re.escape(word))

# 7. megkeressük az átírt adatot a listán = illesztjük regex-t list-re

                compiled_regex = re.compile(regex)
                matches = list(filter(compiled_regex.fullmatch, terms))

# 8. ha van találat: visszaadjuk az összes találatot + ratio()!

                if matches:
                    if len(matches) == 1:
                        res = matches[0]
                    elif len(matches) > 1:
                        # megmérjük strict vs match távot,
                        # és hozzáírjuk a szavakhoz: Jóska[0.52],
                        # és sorbatesszük eszerint! :)

                        # lehet szebben? :)
                        res = ';'.join("{}[{:.2f}]".format(i[0], i[1])
                            for i
                            in sorted((
                                (match,
                                 difflib.SequenceMatcher(None, trans, match).ratio())
                                for match
                                in matches),
                                key=lambda x: x[1],
                                reverse=True))

                    result = res + AS_LOOSE
                    transcribed = result
                    cache[word] = result
                    continue

# 9. még teszünk egy próbát a difflib-bel, ha engedélyezve van

                if IS_DIFFLIB: # 
                    close_matches = difflib.get_close_matches(trans, terms, n=1, cutoff=DIFFLIB_CUTOFF)
                    if close_matches:
                        result = trans + FROM_STRICT + ';'.join(close_matches) + AS_DIFFLIB
                        transcribed = result
                        cache[word] = result
                        continue

# 10. egyébként... visszaadjuk trans-t (ami egyértelmű) és kész :)

                result = trans + AS_FALLBACK
                transcribed = result
                cache[word] = result

            transcribed_row[col] = transcribed

        writer.writerow(transcribed_row)


def get_args():
    """Handle commandline arguments."""
    pars = argparse.ArgumentParser(description=__doc__)
    pars.add_argument(
        '-c', '--config',
        required=True,
        help="path to a 'metarules' JSON config file",
    )
    pars.add_argument(
        '-s', '--strict-first-step',
        action='store_true',
        help="add a 'simple strict match' step at the beginning",
    )
    pars.add_argument(
        '-n', '--no-difflib',
        action='store_true',
        help="turn off difflib, no approx search, 7x faster",
    )
    pars.add_argument(
        '-f', '--difflib-cutoff',
        type=float,
        help="cutoff for difflib (default={})".format(DIFFLIB_CUTOFF),
    )
    pars.add_argument(
        '-p', '--plain',
        action='store_true',
        help="do not mark words according to how they handled, do not use this switch if you want to use `make eval*`",
    )
    arguments = pars.parse_args()
    return arguments


def main():
    """Main."""

    args = get_args()

    # ez sztem mehet a get_args()-ba, és csak a config jöjjön ki

    global STRICT_FIRST_STEP
    STRICT_FIRST_STEP = args.strict_first_step

    global IS_DIFFLIB
    IS_DIFFLIB = not args.no_difflib

    global DIFFLIB_CUTOFF
    DIFFLIB_CUTOFF = args.difflib_cutoff if args.difflib_cutoff else 0.8      # set by '-f'
    # XXX hardcoded 0.8 ...

    global IS_MARK
    IS_MARK = not args.plain

    if not IS_MARK:
        global AS_STRICT
        global AS_LOOSE
        global AS_DIFFLIB
        global AS_FALLBACK
        AS_STRICT = ''
        AS_LOOSE = ''
        AS_DIFFLIB = ''
        AS_FALLBACK = ''

    infrastructure = build_infrastructure(args.config)
    process(infrastructure)


if __name__ == '__main__':
    main()
