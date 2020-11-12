# -*- coding: utf-8 -*-
"""Convert 'metarules plain txt' format into specific JSON."""

import json
import re
import sys
from collections import OrderedDict

STRPTN_MARK = '/' # <- a mezőben spec stringillesztős szabály van
COL_MARK = '=' # <- a spec string melyik mezőre illesztendő
# pl.
# 6 rules1 rules2 termlist
# = 6. mezőben alkalmazandó dolgok
# 7/6=string rules1 rules2 termlist
# = 7. mezőben alkalmazandó dolgok, ha 6. mező = string (!)

SPLIT_AT = STRPTN_MARK + COL_MARK


def main():
    """Main."""

    # 1. read

    with open(sys.argv[1]) as inputfile:
        lines = [line.rstrip() for line in inputfile]
    lines = [line
             for line in lines
             if line != '' and not line.startswith('#')]

    # 2. process

    processed = OrderedDict()
    for i, line in enumerate(lines):  
        col_strptn, loose, strict, termlist = line.split(' ')

        data_dict = {"loose": loose, "strict": strict, "termlist": termlist}

        col_split = re.split('[{}]'.format(SPLIT_AT), col_strptn)
        if len(col_split) == 3:
            # itt már megvan az eredeti stringillesztés-mentes sor!
            col, col_to_match, strptn = col_split
            processed[col]["strptn"] = {col_to_match: {strptn: data_dict}}
        else:
            processed[col_strptn] = data_dict

    # 3. write

    print(json.dumps(processed, indent=4))

if __name__ == '__main__':
    main()
