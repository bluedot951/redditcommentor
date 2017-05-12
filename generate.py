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


def extendComment(c, token, tagList, revBiMap, targetTag, curInd):
  count = 0
  doesMatch = False

  alreadyTried = set()

  while True:
    randNum = random.random()
    if token not in revBiMap:
      return None
    key = floorKey(revBiMap[token], randNum)
    nextTok = revBiMap[token][key]
    if len(alreadyTried) > 0.5 * len(revBiMap[token]):
      print "giving up"
      return None
    if nextTok in alreadyTried:
      continue
    # print "nextTok", nextTok

    tempSent = c + nextTok

    myTags = nltk.pos_tag(tempSent.split(" "))


    tags = [tag[1] for tag in myTags]

    # print tags
    # print targetTag


    if tags[curInd] == targetTag[curInd]:
      c += nextTok + " "
      tok = nextTok
      doesMatch = True
      break
    else:
      alreadyTried.add(nextTok)

  return c, tok

def makeBiComment2(revBiMap, tagList, sentList):
  def comp(x, tgElem):
    xi = 0
    ti = 0
    while xi < len(x):
      if ti == len(tgElem):
        return False
      if tgElem[ti] == '.' or tgElem[ti] == ',' or tgElem[ti] == ';':
        ti += 1
        continue
      if tgElem[ti] != x[xi]:
        return False
      ti += 1
      xi += 1
    return True
  while(True):
    while(True):

      tagInd = random.randint(0, len(tagList) - 1)

      targetTag = tagList[tagInd]

      count = 0

      while(True):
        c = ""

        token = "[SOC]"

        randNum = random.random()
        key = floorKey(revBiMap[token], randNum)
        token = revBiMap[token][key]

        c += token + " "

        if token not in revBiMap:
          continue

        randNum = random.random()
        key = floorKey(revBiMap[token], randNum)
        token = revBiMap[token][key]

        c += token + " "

        # print c

        myTags = nltk.pos_tag(c.split(" ")[:-1])


        tags = [tag[1] for tag in myTags]

        # print tags, targetTag


        # doesMatch = comp(targetTag, tags)
        doesMatch = targetTag[0] == tags[0] and targetTag[1] == tags[1]

        # print doesMatch

        if doesMatch:
          break

        count += 1
        if count > 100:
          # print "out of time...\n\n\n"
          break
      if doesMatch:
        break

      # print c

    print "Generating a comment with grammar:", tagList[tagInd]
    print "Grammar based off of:", sentList[tagInd]

    print c
    print tags

    curInd = 2

    giveUpCount = 0
    for curInd in range(2, len(targetTag)):
      out = extendComment(c, token, tagList, revBiMap, targetTag, curInd)
      if out == None:
        giveUpCount += 1
        break
      else:
        if curInd == len(targetTag) - 1:
          return c
      c, tok = out
      if targetTag[curInd+1] == '.':
        c += "."
        print c
        return c
      print c

  return "hello"

# Generates a new comment body based on the bigrams technique using the
# specified bigram reverse-mapping dictionary.
#   - [revUniMap]: The dictionary where words are mapped to dictionaries of
#                  probabilities and words.
def makeBiComment(revBiMap, tagList):
  def comp(x, tgElem):
    xi = 0
    ti = 0
    while xi < len(x):
      if ti == len(tgElem):
        return False
      if tgElem[ti] == '.' or tgElem[ti] == ',' or tgElem[ti] == ';':
        ti += 1
        continue
      if tgElem[ti] != x[xi]:
        return False
      ti += 1
      xi += 1
    return True

  def exact(x, tgElem):
    xi = 0
    ti = 0
    while xi <= len(x):
      if ti == len(tgElem) and xi == len(x):
        return True
      status = True
      for item in tgElem[ti+1:]:
        status &= (item == '.' or item == ',' or item == ';')
      if ti == len(tgElem) or xi == len(x):
        return (status and len(tgElem) > len(x))
      if tgElem[ti] == '.' or tgElem[ti] == ',' or tgElem[ti] == ';':
        ti += 1
        continue
      if tgElem[ti] != x[xi]:
        return False
      ti += 1
      xi += 1
    return False

  def regen(x, tgElem, txt):
    words = txt.split()
    for i in range(len(tgElem)):
      if tgElem[i] == '.' or tgElem[i] == ',' or tgElem[i] == ';':
        words.insert(i, tgElem[i])
    cmt = " ".join(words)
    print cmt
    return cmt

  while True:
    c = ""
    token = ""

    randNum = random.random()
    key = floorKey(revBiMap["[SOC]"], randNum)
    token = revBiMap["[SOC]"][key]

    c += token + " "

    breakout = False
    while True:
      randNum = random.random()
      if token not in revBiMap:
        breakout = True
        break
      key = floorKey(revBiMap[token], randNum)
      if key in revBiMap[token]:
        break
    if breakout:
      continue
    token = revBiMap[token][key]

    c += token + " "

    tempC = c

    tempTags = nltk.pos_tag(tempC.split())
    tempTags = [i[1] for i in tempTags]

    oldTagList = tagList
    tagList = filter(lambda x: comp(tempTags, x), tagList)

    if len(tagList) == 0:
      tagList = oldTagList
      continue

    breakout = False
    while True:
      randNum = random.random()
      if token not in revBiMap:
        breakout = True
        break
      key = floorKey(revBiMap[token], randNum)
      if key in revBiMap[token]:
        break
    if breakout:
      continue
    token = revBiMap[token][key]

    count = 2

    num_tries = 0

    while True:
      tempC = c + token

      tempTags = nltk.pos_tag(tempC.split())
      tempTags = [i[1] for i in tempTags]
      oldTagList2 = tagList

      tagList = filter(lambda x: comp(tempTags, x), tagList)

      print "token: ", token
      print "tempC: ", tempC
      print "tagList: ", tagList

      if len(tagList) == 0:
        tagList = oldTagList2
        num_tries += 1
        if num_tries > 10:
          tagList = oldTagList
          break
        count = 2
        continue

      count += 1

      c += token + " "
      breakout = False
      while True:
        randNum = random.random()
        if token not in revBiMap:
          breakout = True
          break
        key = floorKey(revBiMap[token], randNum)
        if key in revBiMap[token]:
          break
      if breakout:
        break
      token = revBiMap[token][key]

      for tag in tagList:
        if exact(tag, tempTags):
          print (tag, tempTags)
          return regen(tempTags, tag, c)

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

  # Join the list of words to create a sentence.
  return " ".join(c[1:])
