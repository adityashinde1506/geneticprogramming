import random
import copy
import gplib


class ai:
	
	def __init__(self,parameters,population,nodelist,function):
		self.function=function
		self.nodelist=nodelist
		self.population=population
		self.parameters=parameters
	
	def generate_population(self,depth):
		self.depth=depth
		trees=[]
		tree=gplib.Tree(self.nodelist)
		for i in range(self.population): 
			trees.append(tree.generate_random(self.parameters,self.depth,0.5))
		return trees

	def mutate(self,tree,probability=0.1):
		if random.random()<probability:
			return gplib.Tree(self.nodelist).generate_random(self.parameters,self.depth)
		else:
			mutated_tree=copy.deepcopy(tree)
			if isinstance(tree,gplib.node):
				mutated_tree.branches=[self.mutate(branch,probability) for branch in mutated_tree.branches]
			return mutated_tree

	def crossover(self,tree1,tree2,probability=0.7,root=1):
		if random.random()<probability and not root:
			return copy.deepcopy(tree2)
		else:
			result=copy.deepcopy(tree1)
			if isinstance(tree1,gplib.node) and isinstance(tree2,gplib.node):
				result.branches=[self.crossover(branch,random.choice(tree2.branches),probability,0) for branch in tree1.branches]
			return result

	def evolve(self,population,evalfunction,prob_crossover=0.7,prob_mutation=0.1,prob_new=0.05,maxgenerations=1000,offsprings=1000):
		print evalfunction
		gen=0
		last=None
		end=maxgenerations
		while maxgenerations:
			best,scores=evalfunction(population,self.function)
			print "Generation: %d | Got best score %d | "%(gen,scores[0])
			if scores[0]==0.00:
				break
			nextgen=[]
			nextgen.append(best[0])
			nextgen.append(best[1])
			while len(nextgen)<offsprings:
				if random.random()<prob_new:
					nextgen.append(gplib.Tree(self.nodelist).generate_random(self.parameters,self.depth))
				elif random.random()<prob_mutation:
					nextgen.append(self.mutate(random.choice(best)))
				elif random.random()<prob_crossover:
					nextgen.append(self.crossover(random.choice(best[:100]),random.choice(best[:100])))
			population=nextgen
			maxgenerations-=1
			gen+=1
#			if gen%200 == 0:
#				print '\n\n\n\n\n yes \n\n\n\n'
#				if scores[0]==last:
#					print "\n\nEvolution reached maxima..."
#					print "Restarting from new population "
#					if raw_input("Generate new population? (y/n)") == 'n':
#						break
#					population=self.generate_population(self.depth)
#					maxgenerations=end
#					gen=0
#				last=scores[0]
				
		return scores[0],best[0]
				
			
		
			
			
