import sys
import time
import pickle

from parse import *
from utils import *
from generate import *
from pipetools import pipe
from pipetools.utils import foreach
from tqdm import tqdm

# Number of comments to generate.
NUM_COMMENTS = 1

# Number of "grams" to use in comment generation.
N = 2

# Status flag on whether or not the data has been pickled.
#   - [C_PICKLED]: For whether comments have been pickled.
#   - [T_PICKLED]: For whether the actual tree has been pickled.
C_PICKLED = True
T_PICKLED = False

# Testing arena for the n-gram comment generation.
def main(argv):
  # Start the timer.
  start = time.time()

  # Initially, there are no loaded comments.
  comments = None

  # Initially, there is no tree (or map).
  revTree = None

  if not C_PICKLED:
    # The list of files to learn the model on.
    dir = "data/comments/"
    files = [dir + "2005-12.txt"]
    for i in range(6,9):
      for j in range(1,13):
        files.append(dir + "20" + str(i).zfill(2) + "-" + str(j).zfill(2) + ".txt")

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

    # Dump the comments to a pickle ("jar") for easy re-use.
    print "Pickling comment structure..."
    for _ in tqdm(range(1)):
      outfile = open('data/comments.pkl', 'wb')
      pickle.dump(comments, outfile)
      outfile.close()
  else:
    print "Loading pickled comment structures..."
    for _ in tqdm(range(1)):
      infile = open('data/comments.pkl', 'r')
      comments = pickle.load(infile)
      infile.close()

  # We only want to generate the data structure if we really have to.
  if not T_PICKLED:
    # Empty lambda-expression for now.
    makeTree = lambda _: None

    # Uses OCaml-style composition to create a function from comments to a tree.
    if N == 1:
      makeTree = (pipe
        | getUnigrams
        | getRevUniMap
      )
    else:
      makeTree = (pipe
        | (lambda x: getTree(N, x))
        | normalize
        | getReverseTree
      )

    # Only create the tree (map) once to avoid repeated computation.
    revTree = makeTree(comments)

    # Dump the structure to a pickle ("jar") for easy re-use.
    print "Pickling data structures..."
    for _ in tqdm(range(1)):
      outfile = open('data/' + str(N) + '-grams.pkl', 'wb')
      pickle.dump(revTree, outfile)
      outfile.close()
  else:
    print "Loading pickled data structures..."
    for _ in tqdm(range(1)):
      infile = open('data/' + str(N) + '-grams.pkl', 'r')
      revTree = pickle.load(infile)
      infile.close()

  # Open up a file channel to write the comments to.
  out = open('comments.txt', 'w')

  # Generate NUM_COMMENTS comments.
  print "Generating comments..."
  for i in tqdm(range(NUM_COMMENTS)):
    # Initially, the body is empty.
    body = None

    # Special case when N = 1: generate a unigram-based comment.
    if N == 1:
      body = makeUniComment(revTree)
    else:
      body = makeNComment(N, revTree)

    comment = Comment(body)
    out.write(str(comment))
  
  out.write('\n')
  out.close()

  # End the timer.
  end = time.time()
  totTime = end - start

  # Give the running time in sec or msec, whichever is more readable.
  if totTime >= 3600.:
    hourTime = totTime / 3600.
    hours = int(hourTime)
    minTime = 60. * (hourTime - float(hours))
    mins = int(minTime)
    secs = 60. * (minTime - float(mins))
    print "Running time: %s h, %s m, %s s" % (hours, mins, secs)
  elif totTime >= 60.:
    minTime = totTime / 60.
    mins = int(minTime)
    secs = 60. * (minTime - float(mins))
    print "Running time: %s m, %s s" % (mins, secs)
  elif totTime >= 0.1:
    print "Running time: %s s" % totTime
  else:
    print "Running time: %s ms" % (totTime * 1000.)

if __name__ == "__main__":
  main(sys.argv)
