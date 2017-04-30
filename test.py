import sys
import time

from parse import *
from utils import *
from generate import *
from pipetools import pipe
from pipetools.utils import foreach

# Number of comments to generate.
NUM_COMMENTS = 1
N = 1

# Testing arena for the n-gram comment generation.
def main(argv):
  # Start the timer.
  start = time.time()

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

  # print "revTree", revTree

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