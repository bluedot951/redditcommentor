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

# Number of "grams" to use in comment generation.
N = 1

# Status flag on whether or not the data has been pickled.
PICKLED = False

# Testing arena for the n-gram comment generation.
def main(argv):
  # Start the timer.
  start = time.time()

  # Initially, there is no tree (or map).
  revTree = None

  # We only want to generate the data structure if we really have to.
  if not PICKLED:
    # The list of files to learn the model on.
    files = ["data/2005-12.txt"]
    for i in range(6,9):
      for j in range(1,13)
        files.append("data/20" + str(i).zfill(2) + "-" + str(j).zfill(2) + ".txt")

    # Empty lambda-expression for now.
    makeTree = lambda _: None

    # We need to specifically use unigrams if N is 1.
    # Uses OCaml-style composition to create a function from files to a tree.
    if N == 1:
      makeTree = (pipe
        | getData
        | convertToUTF
        | toComment
        | foreach (sanitize)
        | list
        | getUnigrams
        | getRevUniMap
      )
    else:
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
    
    # Dump the structure to a pickle ("jar") for easy re-use.
    outfile = open('data/' + str(N) + 'grams.pkl', 'wb')
    pickle.dump(revTree, outfile)
    outfile.close()
  else:
    infile = open('data/' + str(N) + 'grams.pkl', 'r')
    revTree = pickle.load(infile)
    infile.close()

  # Open up a file channel to write the comments to.
  out = open('comments.txt', 'w')

  # Generate NUM_COMMENTS comments.
  for i in range(NUM_COMMENTS):
    # Initially, the body is empty.
    body = None

    # Special case when N = 1: generate a unigram-based comment.
    if N == 1:
      body = makeUniComment(revTree)
    else:
      body = makeNComment(N, revTree)

    comment = Comment(body)
    out.write(str(comment))

  out.close()

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
