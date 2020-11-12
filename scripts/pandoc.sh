#!/bin/bash

IN=$1
OUT=$2

pandoc \
--highlight-style scripts/customize.theme \
--include-in-header scripts/customize.tex \
--variable classoption:12pt \
--variable geometry:a4paper \
--variable geometry:margin=2.5cm \
--variable mainfont:Amiri-Regular \
--variable monofont:DejaVuSansMono \
--variable colorlinks \
--variable linkcolor:darkgray \
--variable linkbordercolor:darkgray \
--pdf-engine xelatex \
$IN -s -o $OUT

# itt persze lehet .tex kimenet, és azt tetszőlegesen alakítgatni!
#README.md -s -o README.tex

# az Amiri-Regular tök jó! :)

#--toc \
#--variable toccolor:darkgray \
#--variable toc-title:Tartalom \

