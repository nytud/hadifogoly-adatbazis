#!/bin/bash
# https://www.gnu.org/software/coreutils/manual/html_node/Random-sources.html

seed="$1"
openssl enc -aes-256-ctr -pass pass:"$seed" -nosalt \
</dev/zero 2>/dev/null

