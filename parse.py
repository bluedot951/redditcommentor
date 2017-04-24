import json

# yaml returns dictionaries of strings (rather than unicode, as json does), but seems 200x slower...
import yaml
import time
import collections

# converts keys and values of dictionary from unicode to utf-8
def convert(data):
	newData = []
	for i, item in enumerate(data):
		try:
			newDict = {}
			for k in item:
				# print "k", k
				# print "item[k]", item[k]
				# print str(k)
				newDict[str(k)] = str(item[k])
			# print type(item)
			newData.append(newDict)
		except:
			print("exception!")
	return newData


a = time.time()

data = open("RC_2005-12.txt", "r").read().split("\n")

print len(data)

# 1/0

strdata = '[' + ','.join(data) + ']'

# print data
# print len(data)

parsedData = json.loads(strdata)

parsedData = convert(parsedData)

print len(parsedData)

# print parsedData[0]

b = time.time()

maxUps = -1
best = None

for comm in parsedData:
	up = int(comm['ups'])
	if up > maxUps:
		maxUps = up
		best = comm

print best
print best.keys()

print b-a