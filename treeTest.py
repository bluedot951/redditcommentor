import utils
# import generate

commentlist = ["[SOC] a b c a c b a c [EOC]"]
# commentlist = ["a b a d"]

myTree = utils.getTree(3, commentlist)

# print myTree

utils.normalize(myTree)

print myTree

utils.getReverseTree(myTree)

print myTree



# print myTree.printReverseMap()