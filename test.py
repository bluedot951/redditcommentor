import sys
import time
import pickle

from parse import *
from utils import *
from generate import *
from pipetools import pipe
from pipetools.utils import foreach

# Number of comments to generate.
NUM_COMMENTS = 1
N = 2
PICKLED = True

# Testing arena for the n-gram comment generation.
def main(argv):
  # Start the timer.
  start = time.time()

  if not PICKLED:
    # The list of files to learn the model on.
    files = ["data/2005-12.txt"]
    for i in range(1,13):
      files.append("data/2006-" + str(i).zfill(2) + ".txt")

    # OCaml-style composition to create a function from files to a reverse-map.
    makeTree = (pipe
      | getData
      | convertToUTF
      | toComment
      | foreach (sanitize)
      | list
      | (lambda x: getTree(N, x))
      | normalize
      | getReverseTree
    )

    # Only create the map once to avoid repeated computation.
    revTree = makeTree(files)

    outfile = open('data/2006-4grams.pkl', 'wb')
    pickle.dump(revTree, outfile)
    outfile.close()
  else:
    infile = open('data/2006-4grams.pkl', 'r')
    revTree = pickle.load(infile)
    infile.close()

  # Generate NUM_COMMENTS comments.
  for i in range(NUM_COMMENTS):
    body = makeNComment(N, revTree)
    comment = Comment(body)
    print(comment)

  # End the timer.
  end = time.time()
  totTime = end - start

  # Give the running time in sec or msec, whichever is more readable.
  if totTime >= 0.1:
    print "Running time: %s s" % totTime
  else:
    print "Running time: %s ms" % (totTime * 1000.)

if __name__ == "__main__":
  main(sys.argv)
