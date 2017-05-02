import random
from utils import floorKey

# Generates a new comment body based on the unigrams technique using the
# specified unigram reverse-mapping dictionary.
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

# Generates a new comment body based on the bigrams technique using the
# specified bigram reverse-mapping dictionary.
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

# Generates a new comment body based on the N-grams technique using the
# specified gram-tree. Requires a parameter n <= N to be passed in for the
# creation of the comment, where N was used to generate the gram-tree.
#   - [n]:    The number of grams to use when generating the comment.
#   - [tree]: The recursive gram-tree structure to search when generating a
#             comment. Contains both forward and reverse maps as defined above.
def makeNComment(n, tree):
  c = []
  token = "[SOC]"

  while token != "[EOC]":
    # Same set-up as before, except now `c` is a list.
    c.append(token)
    randNum = random.random()
    prevs = c[-n+1:]

    # Walk down the tree using a referenced pointer.
    tempTree = tree
    for word in prevs:
      tempTree = tempTree.forwardMap[word][0]
    
    # Find the probability associated with the generated word.
    key = floorKey(tempTree.reverseMap, randNum)
    token = tempTree.reverseMap[key].word

  # Join the list of words to create a sentence.
  return " ".join(c[1:])
