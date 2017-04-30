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


# n < m, where m was used to construct tree
def makeNComment(n, tree):
  c = []
  token = "[SOC]"

  while token != "[EOC]":
    # print "token:", token

    c.append(token)
    randNum = random.random()

    prevs = c[-n+1:]

    myPointer = tree

    for word in prevs:
      myPointer = myPointer.forwardMap[word][0]

    key = floorKey(myPointer.reverseMap, randNum)

    token = myPointer.reverseMap[key].word

  return " ".join(c[1:])