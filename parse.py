import json

# yaml returns dictionaries of strings (rather than unicode, as json does), but seems 200x slower...
import yaml
import time
import collections
import random

class Comment(object):
	def __init__(self, text, subreddit, score, gilded, controversiality):
		self.text = text
		self.subreddit = subreddit
		self.score = int(score)
		self.gilded = int(gilded)
		self.controversiality = int(controversiality)
	def __str__(self):
		return str( (self.subreddit, self.text, self.score) )
		# return str( (self.subreddit, self.score) )

	__repr__ = __str__

# converts keys and values of dictionary from unicode to utf-8
def convert(data):
	newData = []
	for i, item in enumerate(data):
		try:
			newDict = {}
			for k in item:
				newDict[str(k)] = str(item[k])
			newData.append(newDict)

		except:
			pass
			# print "exception!", i
	return newData

def floorKey(d, key):
	if key in d:
		return key
	return max(k for k in d if k < key)

def getUnigrams(commentList):
	unigrams = {}
	totCount = 0
	for comment in commentList:
		words = comment.text.split()
		totCount += len(words)

		for word in words:
			if word not in unigrams:
				unigrams[word] = 0
			unigrams[word] += 1
	for u in unigrams:
		unigrams[u] /= float(totCount)

	return unigrams

def getRevUniMap(unigrams):
	curProb = 0.0

	reverseMap = {}

	for u in unigrams:
		reverseMap[curProb] = u
		curProb+=unigrams[u]

	return reverseMap

def getBigrams(commentList):
	bigrams = {}
	totCount = 0
	for comment in commentList:
		words = comment.text.split()
		
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

def getRevBiMap(bigrams):

	reverseMap = {}

	for bd in bigrams:
		reverseMap[bd] = getRevUniMap(bigrams[bd])

	return reverseMap

def cleanup(body):
	# print "cleaning"
	# print body
	# print "\n\n"
	body = body.replace("\r", " ")
	body = body.replace("\n", " ")
	# print "cleaned", body
	return body

def makeComment(revMap):
	randNum = random.random()
	key = floorKey(revMap, randNum)
	token = revMap[key]
	c = ""
	while token != "[EOC]":
		c += token + " "
		randNum = random.random()
		key = floorKey(revMap, randNum)
		token = revMap[key]
	return c[:-1]

def makeBiComment(revMap, revBiMap):
	randNum = random.random()
	key = floorKey(revMap, randNum)
	token = revMap[key]
	c = ""

	while token != "[EOC]":
		c += token + " "
		randNum = random.random()
		key = floorKey(revBiMap[token], randNum)
		token = revBiMap[token][key]
	return c[:-1]

a = time.time()

data = open("RC_2005-12.txt", "r").read().split("\n")
# data = open("test.txt", "r").read().split("\n")



strdata = '[' + ','.join(data) + ']'


parsedData = json.loads(strdata)

parsedData = convert(parsedData)


c = Comment("hello world", "subreddit", 10, 0, 0)
# print c



maxUps = -1
best = None

comments = []

for comm in parsedData:
	up = int(comm['ups'])
	if up > maxUps:
		maxUps = up
		best = comm
	# body = comm["body"]
	# print "comm", comm
	# print "body in for"
	# print comm["body"]
	if comm["body"] != "[deleted]" and comm["body"] != "[removed]":
		c = Comment(comm["body"] + " [EOC]", comm["subreddit"], comm["score"], comm["gilded"], comm["controversiality"])
		comments.append(c)

# print best

for comm in comments:
	comm.text = cleanup(comm.text)


# comments = sorted(comments, key = lambda comm: comm.score)


# bodies = [comm.text for comm in comments]

# print comments
# for comm in comments:
# 	print comm.text

# comments = comments[0:10]

# c = comments[0]

# c.body = "a man a plan a canal panama"

# comments = [Comment("a man a plan a canal panama [EOC]", "hi", 0, 0, 0)]

# print comments
revUniMap = getRevUniMap(getUnigrams(comments))

bg = getBigrams(comments)

# print bg
revBiMap = getRevBiMap(bg)

# print revBiMap

total = 0

print makeBiComment(revUniMap, revBiMap)

1/0

for i in range(1):
	c = makeComment(revMap)
	print c
	total += len(c.split())

print total/1.

mykeys = list(revMap.keys())

mykeys.sort()

print mykeys

# for i in mykeys:
# 	print i, revMap[i]

b = time.time()

print "Time: %s" % (b-a)