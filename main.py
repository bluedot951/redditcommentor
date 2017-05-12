import sys
import time
import datetime
import pickle

from parse import *
from utils import *
from generate import *
from pipetools import pipe
from pipetools.utils import foreach
from tqdm import tqdm

# Number of comments to generate.
NUM_COMMENTS = 100
SUBREDDIT = "science"

# Number of "grams" to use in comment generation.
N = 2

# Status flag on whether or not the data has been pickled.
#   - [C_PICKLED]: For whether comments have been pickled.
#   - [T_PICKLED]: For whether the actual tree has been pickled.
C_PICKLED = False
T_PICKLED = False

tm = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d-%H-%M-%S')
OUTFILE = "profiling/comments-" + tm + ".txt"

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
    datadir = "data/comments/"
    # subreddits = ["AskReddit", "news", "science", "aww", "television"]
    files = [datadir + SUBREDDIT + "-2010-01.txt"]

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
      outfile = open('data/' + SUBREDDIT + '-tr-comments.pkl', 'wb')
      pickle.dump(comments, outfile)
      outfile.close()
  else:
    print "Loading pickled comment structures..."
    for _ in tqdm(range(1)):
      infile = open('data/' + SUBREDDIT + '-tr-comments.pkl', 'r')
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
    elif N == 2:
      makeTree = (pipe
        | getBigrams
        | getRevBiMap
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
      outfile = open('data/' + SUBREDDIT + '-' + str(N) + '-grams.pkl', 'wb')
      pickle.dump(revTree, outfile)
      outfile.close()
  else:
    print "Loading pickled data structures..."
    for _ in tqdm(range(1)):
      infile = open('data/' + SUBREDDIT + '-' + str(N) + '-grams.pkl', 'r')
      revTree = pickle.load(infile)
      infile.close()

  # Open up a file channel to write the comments to.
  out = open(OUTFILE, 'w')

  tagList = pickle.load(open('data/tags2.pkl', 'r'))
  sentList = pickle.load(open('data/tagSents2.pkl', 'r'))

  # Generate NUM_COMMENTS comments.
  print "Generating comments..."
  # for i in tqdm(range(NUM_COMMENTS)):
  for i in range(NUM_COMMENTS):
    # Initially, the body is empty.
    body = None

    # Special case when N = 1: generate a unigram-based comment.
    if N == 1:
      body = makeUniComment(revTree)
    elif N == 2:
      body = makeBiComment(revTree, tagList, sentList)
    else:
      body = makeNComment(N, revTree)

    out.write(body)
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
