"""
Extract most frequent forms for manual training data creation.
"""

import argparse
import sys

from collections import defaultdict
from collections import Counter


ALPHABET = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
#ALPHABET = 'абвгдеёжзийклмнопрстуфхцчшщыьэюя' # without ъ (!)

# frequency list of words (Counter???)
words = defaultdict(int)

# we need at least 'count' pieces of every char
# to be able to create well-founded transcription rules
count = 100
needed = defaultdict(int, {char: count for char in ALPHABET})
#
# ъ csak 168 db van az egészben!
# minden másból van 1000<
# ahhoz, hogy minden betűből legyen 100 -> 1612 szó kell


def main():
    """Main."""

    # stdin ->
    for line in sys.stdin:
        lower = line.strip().lower() # lower!
        fields = lower.split('\t')

        # vezetéknév
        words[f'vez\t{fields[1]}'] += 1
        # keresztnév (saját + apai)
        words[f'ker\t{fields[2]}'] += 1
        words[f'ker\t{fields[3]}'] += 1

        # hely: születés
        for word in fields[5].replace(',', '').split(' '):
            words[f'hly\t{word}'] += 1
        # hely: elfogás
        for word in fields[6].replace(',', '').split(' '):
            words[f'hly\t{word}'] += 1

    all_covered = False

    # gyak szerint csökkenően végig a gyaklistán
    for elem, cnt in sorted(words.items(), key=lambda item: item[1], reverse=True):
        kind, word = elem.split('\t')

        # kell a szó, ha van benne olyan betű, ami még kell
        # és a betűit elkönyveljük = needed[char] csökkentése
        if any(needed[char] > 0 for char in word):
            for char in word:
                needed[char] -= 1
            print(f'{cnt}\t{kind}\t{word}')

        ## ha minden 0 (semmi se needed), akkor lépjünk ki! :)
        if all(val <= 0 for val in needed.values()):
            all_covered = True
            break

    if all_covered:
        print(f'Mindenből van {count}. :)')
    else:
        print(f'{count}-hoz még kellene: {[item for item in needed.items() if item[1] > 0]}')


if __name__ == '__main__':
    main()

