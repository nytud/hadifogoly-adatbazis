"""
Process training data to generate rules.
"""

import sys

from collections import defaultdict


rules = defaultdict(lambda: defaultdict(int)) # :)


# XXX 1-char kódolás -- lehetne mindenhol
one_chars = {
#    'gy': 'G',
}

# XXX [aáo] --> 'A', azaz ezeket nem különítjük el, mert nehéz!
mergesimplify = {
    'a': 'A',
    'á': 'A',
    'o': 'A',
#    'g': 'H',
#    'h': 'H'
}


def main():
    """Main."""

    # stdin -> stdout identity filter
    for line in sys.stdin:
        fields = line.strip().split('\t')
        if len(fields) < 4:
            continue
        orig, trans = fields[2:4]

        orig = orig.split(' ') if ' ' in orig else [ch for ch in orig]
        trans = trans.split(' ') if ' ' in trans else [ch for ch in trans]

        # ha szeretnénk 1-kar kódolást -- és miért ne
        for ch, one_char in one_chars.items():
            trans = [char.replace(ch, one_char) for char in trans]

        # XXX ha össze akarunk vonni "eldönthetetleneket" egybe
        for ch, merged in mergesimplify.items():
            trans = [char.replace(ch, merged) for char in trans]

        # XXX ha el akarjuk különíteni a szó elejét és végét
        #orig[0] = '^' + orig[0]
        #orig[-1] = orig[-1] + '$'
        #trans[0] = '^' + trans[0]
        #trans[-1] = trans[-1] + '$'

        for a, b in zip(orig, trans): # :)
            rules[a][b] += 1

    # print result with percentages

    # -- eredeti orosz karakter szerint ábécében
    #for orig_char, trans_chars in sorted(rules.items()):

    # -- legnagyobb %-os érték szerint = elöl a nehezen eldönthetők
    for orig_char, trans_chars in sorted(rules.items(),
            key=lambda rule: max(
            d / sum(rule[1].values()) for d in rule[1].values())):

        summa = sum(trans_chars.values())
        print(orig_char, '->', summa,
            [f'{trans_char} {val/summa:.1%}({val})'
            for trans_char, val in
            sorted(trans_chars.items(),
                key=lambda item: item[1],
                reverse=True)])


if __name__ == '__main__':
    main()
