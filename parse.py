import json

# yaml returns dictionaries of strings (rather than unicode, as json does), but seems 200x slower...
import yaml
import time
import collections

class Comment(object):
	def __init__(self, text, subreddit, score, gilded, controversiality):
		self.text = text
		self.subreddit = subreddit
		self.score = int(score)
		self.gilded = int(gilded)
		self.controversiality = int(controversiality)
	def __str__(self):
		# return str( (self.subreddit, self.text, self.score) )
		return str( (self.subreddit, self.score) )

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
			print("exception!")
	return newData


a = time.time()

data = open("RC_2005-12.txt", "r").read().split("\n")

# print len(data)

# 1/0

strdata = '[' + ','.join(data) + ']'

# print data
# print len(data)

parsedData = json.loads(strdata)

parsedData = convert(parsedData)

# print len(parsedData)

c = Comment("hello world", "subreddit", 10, 0, 0)
print c

# print parsedData[0]

b = time.time()

maxUps = -1
best = None

comments = []

for comm in parsedData:
	# up = int(comm['ups'])
	# if up > maxUps:
	# 	maxUps = up
	# 	best = comm
	c = Comment(comm["body"], comm["subreddit"], comm["score"], comm["gilded"], comm["controversiality"])
	comments.append(c)

print comments[0:10]

comments = sorted(comments, key = lambda comm: comm.score)

print comments[0:10]


# print best
# print best.keys()

print b-a