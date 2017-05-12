from parse import *
from pipetools import pipe
from pipetools.utils import foreach
import nltk
import pickle

files = ["2008-01.txt"]

# Uses OCaml-style composition to create a function from files to comments.
getComments = (pipe
  | getData
  | convertToUTF
  | toComment
  | foreach (sanitize)
  | list
)

# Only create the comments once to avoid repeated computation.
comments = getComments(files)

sents = []
numList = []

curNum = 0

print "Generating sentence list..."
for (i, comm) in tqdm(enumerate(comments)):
	# if i == 5:
	# 	break
	mycomm = comm[6:-6]
	sentList = nltk.sent_tokenize(mycomm)
	for sent in sentList:
		sents.append(sent)
		# numList.append(curNum)
		# curNum += 1
	# sents.extend(sentList)

print len(sents)

print sents[10]



# print len(numList)

# 1/0

# print len(sents)

POSs = []

print "Word tokenizing sentences..."
for sent in tqdm(sents):
	POSs.append(nltk.word_tokenize(sent))

# POSs = [nltk.word_tokenize(sent) for sent in sents]

print POSs[10]

# print sents[0]
# print POSs[0]

POS2s = []

print "Computing POS tags..."
for sent in tqdm(POSs):
	POS2s.append(nltk.pos_tag(sent))

# POSs = [nltk.pos_tag(sent) for sent in POSs]

POSs = POS2s

print POSs[10]


tagLists = []

# for sent in POSs[203:207]:
# 	print sent
# 	print comments[sent[0]]

# 1/0


for sent in POSs:
	tagLists.append([i[1] for i in sent])

print tagLists[10]

filteredSents = []
filteredTags = []

print "Filtering sentences..."
for (i, tag) in tqdm(enumerate(tagLists)):
	if ('``' not in tag and '\'\'' not in tag and len(tag) > 4 and len(tag) < 10 and "$" not in tag and tag[-1] == "."):
		filteredSents.append(sents[i])
		filteredTags.append(tagLists[i])


print len(filteredTags), len(filteredSents)
# print filteredSents[20]
# print filteredTags[20]

# for i in range(len(filteredTags)):
# 	print len(filteredTags[i]), len(filteredSents[i].split())

# tagLists = filter(lambda x: ('``' not in x and '\'\'' not in x and len(x) > 4 and "$" not in x and x[-1] == "."), tagLists)

outfile = open("tags2.pkl", "wb")
# # for (i,tag) in enumerate(tagLists):
# # 	outfile.write(str(POSs[i]) + "\n")
# # 	outfile.write(str(tag) + "\n")

# # outfile.close()

pickle.dump(filteredTags, outfile)

outfile.close()

outfile = open("tagSents2.pkl", "wb")
pickle.dump(filteredSents, outfile)
outfile.close()