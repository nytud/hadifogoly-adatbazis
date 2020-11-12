import difflib
import sys

# az alábbi szerint a 'difflib' és a 'Levenshtein' kb. ua
# https://stackoverflow.com/questions/6690739

word1 = sys.argv[1]
word2 = sys.argv[2]

score = difflib.SequenceMatcher(None, word1, word2).ratio()

print(f"{word1}	{word2}	{score}")

