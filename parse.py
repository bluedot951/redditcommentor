import simplejson as json
import re
import collections

from tqdm import tqdm

# A Comment is an abstraction of a Reddit comment. It contains key information
# about that comment's data, such as its actual body, which subreddit it was
# posted to, its score, whether or not it was gilded, and its controversiality
# ratio (usually a variation of the upvotes to downvotes ratio).
#
# A constructor is provided for comment parsing during the JSON decoding process.
class Comment(object):

  # Constructor for a Comment based on the parsed JSON fields.
  def __init__(self, body, subreddit="reddit.com", score=1, gilded=0, controversiality=0):
    self.body = body
    self.subreddit = subreddit
    self.score = int(score)
    self.gilded = int(gilded)
    self.controversiality = int(controversiality)

  # The so-called 'toString' method that prints out the Comment representation.
  def __str__(self):
    return "Subreddit: " + self.subreddit + "\nText: " + self.body + "\nScore: " + str(self.score)

  __repr__ = __str__

# Defines a custom error to be used when there is trouble with parsing JSON.
class ParseError(Exception):
  pass

# Defines a custom error to be used when there is trouble with converting data.
class TokenizeError(Exception):
  pass

# Generates a single JSON object using the specified JSON files as input.
#   - [files]: A list of file names from which the data should be extracted.
# Raises: ParseError if any of the files are not valid JSON.
def getData(files):
  strData = []
  
  print "Parsing files..."
  for file in tqdm(files):
    with open(file, "r") as myf:
      tempStrData = myf.read().split("\n")[:-1]
      strData.extend(tempStrData)
  
  jsonData = '[' + ','.join(strData) + ']'
  
  try:
    data = json.loads(jsonData)
    return data
  except:
    raise ParseError("There was an error in decoding one of the input files.")

# Converts the specified JSON object into a UTF-8 compatible equivalent.
#   - [data]: The JSON object to map from Unicode to UTF-8.
# Raises: TokenizeError if any of the files are not valid JSON.
def convertToUTF(data):
  newData = []

  print "Converting data to UTF-8..."
  for item in tqdm(data):
    try:
      newDict = {}
      for k in item:
        newDict[str(k)] = str(item[k])
      newData.append(newDict)
    except:
      pass # TODO: raise TokenizeError("Unrecognized token: %s" % i)
  
  return newData

# Creates a Comment object out of the specified UTF-8 compatible JSON object
# (i.e. just a plain old dictionary).
#   - [utfData]: A list of UTF-8 compatible JSON dictionaries.
def toComment(utfData):
  comments = []

  print "Classifying comments..."
  for comm in tqdm(utfData):
    # Do not include any comments that were deleted or removed by a moderator.
    if comm["body"] != "[deleted]" and comm["body"] != "[removed]":
      body = "[SOC] " + comm["body"]
      c = Comment(body, comm["subreddit"], comm["score"], comm["gilded"], comm["controversiality"])
      comments.append(c)

  return comments

# Cleans up the body of a comment by removing any new lines, form feeds, links,
# parentheses, and HTML codes (e.g. &nbsp;, &gt;, etc.).
#   - [comment]: The string corresponding to a comment itself (i.e. NOT its body).
def sanitize(comment):
  # Remove newlines
  body = comment.body
  body = body.replace("\r", " ")
  body = body.replace("\n", " ")

  # Remove links
  body = re.sub(r'\[.*\]\(.*\)', '', body)

  # Remove parentheses
  body = body.replace(")", " ")
  body = body.replace("(", " ")

  # Remove HTML codes
  body = body.replace("&gt;", " ")
  body = body.replace("&lt;", " ")
  body = body.replace("&amp;", " ")

  # Remove punctuation
  body = body.replace(",", " ")
  body = body.replace(";", " ")
  body = body.replace(".", " ")

  comment.body = body

  return body
