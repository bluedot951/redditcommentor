import utils

commentlist = ["a b c a c b a c EOF"]
# commentlist = ["a b a d"]

myTree = utils.getTree(3, commentlist)

# print myTree

utils.normalize(myTree)

print myTree

utils.getReverseTree(myTree)

print myTree

# print myTree.printReverseMap()