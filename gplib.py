
import random
import copy

class function:
	def __init__(self,function,name,childcount):
		self.name=name
		self.function=function
		self.childcount=childcount

class node:
	def __init__(self,thefunction,children):
		self.name=thefunction.name
		self.function=thefunction.function
		self.branches=children
		self.childcount=thefunction.childcount

	def evaluate(self,inp):
		setnodes=[child.evaluate(inp) for child in self.branches]
		return self.function(setnodes)
	
	def display_tree(self,indent=0):
		print indent*'  '+self.name
		for child in self.branches:
			child.display_tree(indent+1)

class constant:
	def __init__(self,value):
		self.name='constant '+str(value)
		self.value=value

	def evaluate(self,inp):
		return self.value
	
	def display_tree(self,indent=0):
		print indent*'  '+self.name

class variable:
	def __init__(self,index):
		self.name='variable element '+str(index) 
		self.index=index

	def evaluate(self,inp):
		return inp[self.index]
	
	def display_tree(self,indent=0):
		print indent*'  '+self.name

class Tree:
	def __init__(self,nodelist):
		self.nodelist=nodelist
	
	def generate_random(self,paras,depth,probability=0.5):
		chance=random.random()
#		print depth
		if chance<probability and depth>1:
			root=random.choice(self.nodelist)
			children=[self.generate_random(paras,depth-1,probability) for i in range(root.childcount)]
#			print root
#			print children
			return node(root,children)
		elif chance<0.8:
			return variable(random.randint(0,paras-1))
		else:
#			print 'constant'
			return constant(random.randint(1,10))

	def display_tree(self,indent=0):
		print indent*'  '+str(self.name)
		for child in node.branches:
			child.display_tree(indent+1)
	
				
class Performance:
	def _getdifference(self,result,value):
		return abs(result-value)

	def getscore(self,tree,function):
		diff=0
		for dataset in function:
			diff+=self._getdifference(tree.evaluate(list(dataset[:-1])),dataset[-1:][0])
		return diff

	def getrank(self,trees,function,evalfunction):
		scores=[]
		sortedscores=[]
		best=[]
		for tree in trees:
			scores.append(evalfunction(tree,function))
		sortedscores=scores[:]
		sortedscores.sort()
		for score in sortedscores:
			best.append(trees[scores.index(score)])
#		print sortedscores
		return best,sortedscores

















