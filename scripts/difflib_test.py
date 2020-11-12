import difflib
import sys

# import edit_distance
# https://pypi.org/project/edit-distance -- jól néz ki! :)
# ... viszont sajna nincs get_close_matches() eljárása

# import Levenshtein <- ezt nem bírtam feltenni

# az alábbi szerint a 'difflib' és a 'Levenshtein' kb. ua
# https://stackoverflow.com/questions/6690739


termlist = []
with open( sys.argv[1], "r" ) as f:
  termlist = f.read().split() # 5,5M szó

#words = [
#    "Bejlo",       # 'Belár'              rossz
#    "Georg",       # 'Gergő'              rossz (?)
#    "Karl",        # 'Kartal'             rossz
#    "Sitvan",      # 'Kirtan'             rossz
#    "Roza",        # 'Kozma'              rossz
#    "Pauly",       # 'Saul'               rossz
#    "Miklas",      # 'Miklós'             jó
#    "Ioszif",      # ... nincs tipp       rossz
#    "Dejnes",      #	'Dienes', 'Dénes'   rossz (2. jó)
#    "Bolas",       # 'Béla'               rossz
#    "Balas",       # 'Balassa'            rossz
#    "Szilyvesztr", # 'Szilveszter'        jó
#    "Sando",       # 'Sándor'             jó
#    "Petrovics",   # 'Petrik'             rossz
#    "Petr"         # 'Petúr'              rossz
#]
#
# 3/15 jó = 20%
# ezt sztem nem nagyon érdemes csinálni,
# mert hülyeségre alakítja... XXX XXX XXX

word = sys.argv[2]

best_matches = difflib.get_close_matches(
    word,
    termlist,
    n=int(sys.argv[4]),
    cutoff=float(sys.argv[3]))

for best_match in best_matches:
    score = difflib.SequenceMatcher(None, word, best_match).ratio()
    print(f"{word}	{best_match}	{score}")

