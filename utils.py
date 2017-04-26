from parse import *

# Returns the key if it is in the dictionary or the closest approximation if it
# is not in the dictionary.
#   - [d]: The dictionary in which to search.
#   - [key]: The key being search for.
#            Requires: type(key) == float.
def floorKey(d, key):
  if key in d:
    return key
  return max(k for k in d if k < key)

# Generates a dictionary mapping of words to their associated probabilities
# (i.e. normalized counts) of occurring in the specified comment list.
#   - [commentList]: The list of comments.
def getUnigrams(commentList):
  unigrams = {}
  totCount = 0

  for comment in commentList:
    words = comment.split()
    totCount += len(words)

    for word in words:
      if word not in unigrams:
        unigrams[word] = 0
      unigrams[word] += 1

  for u in unigrams:
    unigrams[u] /= float(totCount)

  return unigrams

# Creates a reverse mapping PDF of the words and their probabilities. Returns a
# dictionary based off of the specified unigrams wherein the probabilities are
# now mapped to the words rather than the other way around.
#   - [unigrams]: The dictionary of mappings between words and probabilities.
def getRevUniMap(unigrams):
  curProb = 0.0
  reverseMap = {}

  for u in unigrams:
    reverseMap[curProb] = u
    curProb += unigrams[u]

  return reverseMap

# Generates a dictionary mapping of words to dictionaries of successive words and
# their associated probabilities (i.e. normalized counts) of occurring in that
# order in the specified comment list.
#   - [commentList]: The list of comments.
def getBigrams(commentList):
  bigrams = {}
  totCount = 0

  for comment in commentList:
    words = comment.split()
    
    for i in range(len(words)-1):
      word = words[i]
      nextWord = words[i+1]

      if word not in bigrams:
        bigrams[word] = {}
      innerDict = bigrams[word]

      if nextWord not in innerDict:
        innerDict[nextWord] = 0
      innerDict[nextWord] += 1

      bigrams[word] = innerDict

  for bd in bigrams:
    mydict = bigrams[bd]
    total = sum(mydict.values())

    for w in mydict:
      mydict[w] /= float(total)

    bigrams[bd] = mydict

  return bigrams

# Creates a reverse mapping PDF of the words and their probabilities. Returns a
# dictionary based off of the specified bigrams wherein the words are
# now mapped to other dictionaries. Each such secondary dictionary is a unigram
# reverse map, and contains probabilities of adjacent occurrence mapped to words.
#   - [bigrams]: The dictionary of mappings between words and dictionaries of
#                words and probabilities.
def getRevBiMap(bigrams):
  reverseMap = {}

  for bd in bigrams:
    reverseMap[bd] = getRevUniMap(bigrams[bd])

  return reverseMap