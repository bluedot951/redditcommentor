from parse import *
from tqdm import tqdm

# A Tree is an abstraction that represents N-way trees in general. It keeps
# track of its children in two different ways, both of which use dictionaries:
#   1. A forward mapping from words to a tuple of (subtree, count).
#   2. A reverse mapping from probabilities to subtrees. No words here.
# Each Tree node also has a word associated with it.
#
# A constructor is provided for initialization.
class Tree(object):

  # Constructor for the Tree based on a word to set as the root. Usually [SOC].
  def __init__(self, word):
    self.word = word
    self.forwardMap = {} # Mapping from word to (tree, count)
    self.reverseMap = {} # Mapping from probabilities to trees

  # The so-called 'toString' method that prints out the Tree representation.
  def __str__(self):
    return "({0}, {1})".format(self.word, str(self.reverseMap))

  __repr__ = __str__

# Creates a subtree in the specified Tree by using the specified key as the
# word for that node. The subtree's mappings are empty.
#   - [tree]: The tree structure in which the subtree should be created.
#   - [key]:  The word to insert for the subtree that will be created.
def createSubTree(tree, key):
  if key in tree.forwardMap:
    return tree.forwardMap[key]
  else:
    tree.forwardMap[key] = [Tree(key), 0]

# Converts the specified comment list into a gram-tree based on the specified n
# value. The forward mapping is filled in at each level, and the returned Tree
# has empty mappings at each of its leaves.
#   - [n]:           The number of grams to use when generating the Tree.
#   - [commentList]: The list of comments from which the Tree is to be created.
def getTree(n, commentList):
  # Initialize an empty Tree. The initial word is always "root".
  root = Tree("root")
  
  if n == 3:
    print "Generating trigrams..."
  else:
    print "Generating " + str(n) + "-grams..."
  
  for (i, comment) in enumerate(tqdm(commentList)):
    # Generate the list of all possible n-grams (consecutive sublists):
    
    words = comment.split()
    ngrams = [words[i:i+n] for i in xrange(len(words)-n+1)]

    # Iterate through the list of all possible n-grams:
    for ngram in ngrams:
      # Walk down the tree using a referenced pointer.
      tempTree = root

      for word in ngram:
        createSubTree(tempTree, word)
        tempTree.forwardMap[word][1] += 1
        tempTree = tempTree.forwardMap[word][0]

  # Return the created Tree, not the referenced pointer.
  return root

# Normalizes the specified tree structure's forward mapping by moving the counts
# to probabilities. Recursive.
#   - [tree]: The tree whose forward mapping is to be normalized.
def normalize(tree):

  # Basis case.
  if len(tree.forwardMap) == 0:
    return

  # Recursive case.
  tot = 0
  for sub in tree.forwardMap:
    tot += tree.forwardMap[sub][1]

  # Walk down the subtrees and normalize the counts on this level.
  for sub in tree.forwardMap:
    tree.forwardMap[sub][1] /= float(tot)

  # Recursively consider the list of subtrees for each subtree on this level.
  for sub in tree.forwardMap:
    normalize(tree.forwardMap[sub][0])

  return tree

# Fills in the reverse mapping for the specified gram-tree by using its forward
# mapping as a guide. The numbers in the forward tree are assumed to be
# normalized, i.e. probabilities rather than counts. Recursive.
#   - [tree]: The gram-tree to traverse and generate the reverse mapping for.
def getReverseTree(tree):

  # Basis case.
  if len(tree.forwardMap) == 0:
    return

  # Recursive case.
  curProb = 0.0

  # Walk down the subtrees and fill in the reverse mappings on this level.
  for sub in tree.forwardMap:
    tree.reverseMap[curProb] = tree.forwardMap[sub][0]
    curProb += tree.forwardMap[sub][1]

  # Recursively consider the list of subtrees for each subtree on this level.
  for sub in tree.forwardMap:
    getReverseTree(tree.forwardMap[sub][0])

  return tree

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

  print "Generating unigrams..."
  for comment in tqdm(commentList):
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

  print "Generating bigrams..."
  for comment in tqdm(commentList):
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
