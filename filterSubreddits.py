from parse import *

files = ["2008-01.txt"]

interestingSubreddits = ["sports", "AskReddit", "gsaming", "javascript", "news"]

allsubreddits = set()

for curMonth in files:

	subreddits = {i: [] for i in interestingSubreddits}
	# subreddits = {'reddit.com':[], 'AskReddit':[]}

	comments = getData(files)

	for comment in comments:
		allsubreddits.add(comment['subreddit'])
		if comment['subreddit'] in subreddits:
			subreddits[comment['subreddit']].append(comment)

	# print subreddits

	for subreddit in subreddits:
		myf = open(subreddit + "-" + curMonth, "w")
		print >>myf, json.dumps(subreddits[subreddit])
		# print "\n\n\/n"
		# print subreddits[subreddit]
		myf.close()

print allsubreddits