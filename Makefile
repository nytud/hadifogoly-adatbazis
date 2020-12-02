
SHELL:=/bin/bash

all:
	@echo "choose explicit target = type 'make ' and press TAB"

S=scripts


# ===== MAIN STUFF 

# >>> mindent egybe <<
# transcribe + eval részletes kiértékeléssel
transcribe_and_eval_by_col: transcribe eval_by_col

# transcribe + eval egyszerű kiértékeléssel
transcribe_and_eval: transcribe eval


# ===== TRANSCRIBE

FILE=Kart_1000_Sor
DATADIR=data
OUTDIR=out
METARULES=rules/metarules.json
FLAGS=
INPUT=$(DATADIR)/$(FILE).csv
INPUT_PREPROCESSED=$(DATADIR)/$(FILE).preprocessed.csv
OUTPUT=$(OUTDIR)/$(FILE).transcribed.new.csv
# prereq: make preparation
transcribe: preprocess
	@echo "--- $@" 1>&2
	@cat $(INPUT_PREPROCESSED) | python3 $S/transcribe.py -c $(METARULES) $(FLAGS) > $(OUTPUT)

# helyek felbontása + zárójeles nevek elhagyása
# sorrend! preextract.py -> ... -> omit_parenth_names.py -> preprocess.py 
preprocess:
	@echo "--- $@" 1>&2
	@cat $(INPUT) | python $S/preextract.py | python3 $S/separate_location_parts.py | python3 $S/omit_parenth_names.py | python3 $S/preprocess.py > $(INPUT_PREPROCESSED)

preparation: convert_rules convert_metarules
	@echo "--- $@" 1>&2

SPLITDIR=splits
SPLIT_FROM=0
SPLIT_TO=2399
SPLIT_OUT=o
SPLIT_ERR=e
# egy csomó minden a scriptben van beállítva...
split_and_parallel: preparation
	@echo "--- $@" 1>&2
	rm -rf $(SPLITDIR) ; date ; time $S/split_and_parallel.sh $(SPLIT_FROM) $(SPLIT_TO) > $(SPLIT_OUT) 2> $(SPLIT_ERR) ; date


# ===== EVAL


EVAL_INPUT=out/$(FILE).transcribed.new.csv
EVAL_OUTPUT=out/$(FILE).eval.new.out
EVAL_ORIG=out/$(FILE).eval.out
eval:
	@echo "--- $@" 1>&2
	@$S/eval.sh $(EVAL_INPUT) > $(EVAL_OUTPUT)
	@cat $(EVAL_OUTPUT) | grep "YES"

eval_diff:
	@echo "--- $@" 1>&2
	@tkdiff $(EVAL_ORIG) $(EVAL_OUTPUT)

EVAL_BY_COL_OUTPUT=out/$(FILE).eval_by_col.new.out
EVAL_BY_COL_ORIG=out/$(FILE).eval_by_col.out
# cols (2-4,6-9,13-16) info in scripts/eval.sh
eval_by_col: eval
	@echo "--- $@" 1>&2
	@( cat $(EVAL_OUTPUT) | grep "YES" ; for COL in 2 3 4 $$(seq 6 9) $$(seq 13 16) ; do echo -n "=== $$COL " ; cat $(EVAL_INPUT) | cut -d '	' -f $$COL > ei.$(FILE); make EVAL_INPUT=ei.$(FILE) EVAL_OUTPUT=eo.$(FILE) eval | grep "darab%" ; echo ; done ) > $(EVAL_BY_COL_OUTPUT) ; rm -f ei.$(FILE) eo.$(FILE)

eval_by_col_diff:
	@echo "--- $@" 1>&2
	@tkdiff $(EVAL_BY_COL_ORIG) $(EVAL_BY_COL_OUTPUT)


# ===== RULES & LISTS


# XXX itt az összes szabályrendszer kezelendő, amit használunk!
convert_rules:
	@echo "--- $@" 1>&2
	@python3 $S/rules2json.py rules/ru2hu
	@python3 $S/rules2json.py rules/ru2de
	@python3 $S/rules2json.py rules/nat

METARULES_INPUT=rules/metarules.txt
METARULES_OUTPUT=rules/metarules.json
convert_metarules: complete_counties_list complete_places_list complete_places_list_de
	@echo "--- $@" 1>&2
	@python3 $S/metarules2json.py $(METARULES_INPUT) > $(METARULES_OUTPUT)

LISTSDIR=data/lists
COUNTIES_INPUT=$(LISTSDIR)/*megyek*
COUNTIES_OUTPUT=$(LISTSDIR)/counties.csv
complete_counties_list:
	@echo "--- $@" 1>&2
	@cat $(COUNTIES_INPUT) | cut -d '	' -f 1 | sort -u > $(COUNTIES_OUTPUT)

PLACES_INPUT=$(LISTSDIR)/*telepules* $(LISTSDIR)/*helyseg*
PLACES_OUTPUT=$(LISTSDIR)/places.csv
complete_places_list:
	@echo "--- $@" 1>&2
	@cat $(PLACES_INPUT) | cut -d '	' -f 1 | sort -u > $(PLACES_OUTPUT)

PLACES_DE_INPUT=$(LISTSDIR)/places_de_wikipedia.csv
PLACES_DE_OUTPUT=$(LISTSDIR)/places_de.csv
complete_places_list_de:
	@echo "--- $@" 1>&2
	@cat $(PLACES_DE_INPUT) | cut -d '	' -f 2 | sort -u > $(PLACES_DE_OUTPUT)


# ===== UTILS

DEPLOY_DIR=deploy_dir
DEPLOY_NAME=habt
DEPLOY_TARGET=corpus.nytud.hu:/var/www/habt
deploy: deploy_random README.pdf
	@echo "--- $@" 1>&2
	@$S/deploy.sh $(DEPLOY_DIR)
	@ln -s $(DEPLOY_DIR) $(DEPLOY_NAME)
	@zip -r $(DEPLOY_NAME) $(DEPLOY_NAME)
	@scp -p $(DEPLOY_NAME).zip $(DEPLOY_TARGET)
	@rm -rf $(DEPLOY_DIR) $(DEPLOY_NAME) $(DEPLOY_NAME).zip
	@echo "--- $@" 1>&2

deploy_random:
	@echo "--- $@" 1>&2
	@scp -p data/random_10000_42.csv $(DEPLOY_TARGET)
	@scp -p out/random_10000_42.transcribed.csv $(DEPLOY_TARGET)

README_IN=README.md
README_INTERM=README_for_pandoc_pdf.md
README_OUT=README.pdf
README.pdf: README.md Makefile $S/pandoc.sh $S/customize.theme $S/customize.tex
	@echo "--- $@" 1>&2
	@cat $(README_IN) | sed "s/(#[0-9][0-9]*-/(#/" > $(README_INTERM)
	@$S/pandoc.sh $(README_INTERM) $(README_OUT)
	@rm -f $(README_INTERM)

FULLDATAFILE=$(DATADIR)/full
TEST_SET_OUTPUT=$(DATADIR)/test_set.csv
TEST_SET_OFFSET=427012
TEST_SET_SIZE=1000
test_set:
	@echo "--- $@" 1>&2
	@( cat $(FULLDATAFILE) | head -1 ; cat $(FULLDATAFILE) | tail -n +$(TEST_SET_OFFSET) | head -$(TEST_SET_SIZE) ) > $(TEST_SET_OUTPUT)

SIMPLY_CONFIG=rules/ru2hu_loose.json
SIMPLY_TEXT=Шейкешфегервар
simply_transcript_text:
	@echo "--- $@" 1>&2
	@python3 $S/simply_transcript_text.py $(SIMPLY_CONFIG) $(SIMPLY_TEXT)

TERMFILE=$(LISTSDIR)/mta_utonevek.csv
FOUND=out/$(FILE).found_column$(COLUMN).$(CONFIG).txt
match: ru2hu
	@echo "--- $@" 1>&2
	@python3 $S/match_long_list.py $(TERMFILE) $(REGEXFILE) > $(FOUND)

COLUMN=3
REGEXFILE=out/$(FILE).regex_column$(COLUMN).$(CONFIG).txt
ru2hu_regex: ru2hu
	@echo "--- $@" 1>&2
	@cat $(TRANSCRIBED) | cut -d '	' -f $(COLUMN) | sort -u > $(REGEXFILE)

CONFIG=loose
CONFIGPATH=rules/$(CONFIG).json
TRANSCRIBED=out/$(FILE).$(CONFIG).transcribed
ru2hu:
	@echo "--- $@" 1>&2
	@cat $(INPUT) | python3 $S/ru2hu.py -c $(CONFIGPATH) > $(TRANSCRIBED)

# mintafájlok betűnként -> #5
CHARSFILE=chars_alphabet
DATAFILE=$(DATADIR)/Kart.csv
DATACOLS=1,2,3,4,6,7
FROMDATAFILE=12
CHAR_SAMPLES_OUTDIR=char_samples
CHAR_SAMPLES_OUTDIRTYPE=char_samples_type
EVAL_COUNT=1000
EVAL_SEED=42
create_char_samples:
	@echo "--- $@" 1>&2
	@for CH in $$(cat $(CHARSFILE)) ; do echo "--- $$CH" ; cat $(DATAFILE) | tail -n +$(FROMDATAFILE) | cut -d '	' -f$(DATACOLS) | grep "$$CH" | shuf -n $(EVAL_COUNT) --random-source=<($S/get_seeded_random.sh $(EVAL_SEED)) > $(CHAR_SAMPLES_OUTDIR)/$$CH.txt ; cat $(CHAR_SAMPLES_OUTDIR)/$$CH.txt | tr '	' '\n' | grep $$CH | sort | uniq -c | sort -nr > $(CHAR_SAMPLES_OUTDIRTYPE)/$$CH.type.txt ; done

# pseudo_{size}_{seed}.csv = pszeudoadat készítése
# oszlopcsoportok egymástól független randomizálásával
PSEUDO_SIZE=1000
PSEUDO_SEED=42
create_pseudo:
	@echo "--- $@" 1>&2
	$S/pseudo_data.sh $(DATAFILE) $(PSEUDO_SIZE) $(PSEUDO_SEED) > $(DATADIR)/pseudo_$(PSEUDO_SIZE)_$(PSEUDO_SEED).csv

# random rendes adat készítése
# = n db random sor, sorokon belül persze nincs randomizálás!
RANDOM_SIZE=10000
RANDOM_SEED=42
create_random:
	@echo "--- $@" 1>&2
	$S/random_data.sh $(DATAFILE) $(RANDOM_SIZE) $(RANDOM_SEED) > $(DATADIR)/random_$(RANDOM_SIZE)_$(RANDOM_SEED).csv

# create one crafted data record for testing
# in $(DATADIR)/$(CR_FILE).csv
# for setting CR_FLAGS see $S/create_crafted_data.py -h
# example usage:
# make create_crafted_data CR_FLAGS="-F 'Янош' -H 'д. Парад, обл. Хевеш'"
CR_FILE=crafted
CR_FLAGS=
create_crafted_data:
	@python $S/create_crafted_data.py $(CR_FLAGS) > $(DATADIR)/$(CR_FILE).csv

