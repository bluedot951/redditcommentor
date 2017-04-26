import random
from utils import floorKey

# Generates a new comment body based on the unigrams technique using the specified
# unigram reverse-mapping dictionary.
#   - [revUniMap]: The dictionary where probabilities are mapped to words.
def makeUniComment(revUniMap):
  c = ""
  token = "[SOC]"

  while token != "[EOC]":
    c += token + " "
    randNum = random.random()
    key = floorKey(revUniMap, randNum)
    token = revMap[key]

  # Will always be at least just '', but removes "[SOC]" and " " from string.
  return c[6:-1]

# Generates a new comment body based on the bigrams technique using the specified
# bigram reverse-mapping dictionary.
#   - [revUniMap]: The dictionary where words are mapped to dictionaries of
#                  probabilities and words.
def makeBiComment(revBiMap):
  c = ""
  token = "[SOC]"

  while token != "[EOC]":
    c += token + " "
    randNum = random.random()
    key = floorKey(revBiMap[token], randNum)
    token = revBiMap[token][key]

  # Will always be at least just '', but removes "[SOC]" and " " from string.
  return c[6:-1]