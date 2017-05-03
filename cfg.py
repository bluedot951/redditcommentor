from parse import *
from pipetools import pipe
from pipetools.utils import foreach
import nltk
import pickle

files = ["2005-12.txt"]

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

for (i, comm) in enumerate(comments):
	# if i == 5:
	# 	break
	mycomm = comm[6:-6]
	sents.extend(nltk.sent_tokenize(mycomm))

# print len(sents)

POSs = [nltk.word_tokenize(sent) for sent in sents]

print sents[0]
print POSs[0]

POSs = [nltk.pos_tag(sent) for sent in POSs]

tagLists = []

for sent in POSs[0:2]:
	print sent

for sent in POSs:
	tagLists.append([i[1] for i in sent])

# tagLists = filter(lambda x: ('``' not in x and '\'\'' not in x and len(x) > 4 and "$" not in x and x[-1] == "."), tagLists)

outfile = open("tags.pkl", "wb")
# for (i,tag) in enumerate(tagLists):
# 	outfile.write(str(POSs[i]) + "\n")
# 	outfile.write(str(tag) + "\n")

# outfile.close()

pickle.dump(tagLists, outfile)

outfile.close()