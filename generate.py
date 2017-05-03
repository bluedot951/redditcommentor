import random
from utils import floorKey
import nltk

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
    token = revUniMap[key]

  # Will always be at least just '', but removes "[SOC]" and " " from string.
  return c[6:-1]

# Generates a new comment body based on the bigrams technique using the
# specified bigram reverse-mapping dictionary.
#   - [revUniMap]: The dictionary where words are mapped to dictionaries of
#                  probabilities and words.
def makeBiComment(revBiMap, tagList):
  c = ""

  randNum = random.random()
  key = floorKey(revBiMap["[SOC]"], randNum)
  token = revBiMap[token][key]

  c += token + " "

  randNum = random.random()
  key = floorKey(revBiMap[token], randNum)
  token = revBiMap[token][key]

  c += token + " "

  tempC = c

  tempTags = nltk.pos_tag(tempC.split())
  tempTags = [i[1] for i in tempTags]

  tagList = filter(lambda x: (x[0] == tempTags[0] and x[1] == tempTags[1]), tagList)

  randNum = random.random()
  key = floorKey(revBiMap[token], randNum)
  token = revBiMap[token][key]

  count = 2


  while token != ".":
    print c

    tempC = c + token

    tempTags = nltk.pos_tag(tempC.split())
    tempTags = [i[1] for i in tempTags]
    tagList = filter(lambda x: (x[count] == tempTags[count]), tagList)

    if len(tagList) == 0:
      print "rip"
      1/0

    count += 1

    c += token + " "
    randNum = random.random()
    key = floorKey(revBiMap[token], randNum)
    token = revBiMap[token][key]

  # Will always be at least just '', but removes "[SOC]" and " " from string.
  return c[:-1] + "."

# Generates a new comment body based on the N-grams technique using the
# specified gram-tree. Requires a parameter n <= N to be passed in for the
# creation of the comment, where N was used to generate the gram-tree.
#   - [n]:    The number of grams to use when generating the comment.
#   - [tree]: The recursive gram-tree structure to search when generating a
#             comment. Contains both forward and reverse maps as defined above.
def makeNComment(n, tree, tagList):
  c = []
  token = "[SOC]"

  wordNum = 0

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

    tokenPOS = 

    tagList = 

  # Join the list of words to create a sentence.
  return " ".join(c[1:])
