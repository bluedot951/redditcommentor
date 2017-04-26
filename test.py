import sys
import time

from parse import *
from utils import *
from generate import *
from pipetools import pipe
from pipetools.utils import foreach

# Simple testing area.
def main(argv):
  start = time.time()

  files = ["data/2005-12.txt"]

  makeComment = (pipe
    | getData
    | convertToUTF
    | toComment
    | foreach(lambda c: sanitize(c.body))
    | list
    | getBigrams
    | getRevBiMap
    | makeBiComment
  )

  body = makeComment(files)
  comment = Comment(body)

  print(comment)

  end = time.time()
  totTime = end - start

  if totTime >= 1.0:
    print "Running time: %s s" % totTime
  else:
    print "Running time: %s ms" % (totTime * 1000.)

if __name__ == "__main__":
  main(sys.argv)