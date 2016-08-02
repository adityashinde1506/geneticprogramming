import gplib
import defaults
import evolution
import random
import pickle
import time
import os
import math


class Player:
	def __init__(self,tree,limit,loc=[0,0]):
		self.tree=tree
		self.loc=loc
		self.limit=limit
	def move(self,paras):
		val=self.tree.evaluate(paras)%4			
		if val==0:
			self.loc[0]-=1
			if self.loc[0]<0:
				self.loc[0]=0
		elif val==1:
			self.loc[1]+=1
			if self.loc[1]>self.limit[1]-1:
				self.loc[1]=self.limit[1]-1
		elif val==2:
			self.loc[0]+=1
			if self.loc[0]>self.limit[0]-1:
				self.loc[0]=self.limit[0]-1
		elif val==3:
			self.loc[1]-=1
			if self.loc[1]<0:
				self.loc[1]=0
		return self.loc,val
		

class Trainer(Player):
	__timer=0
	__move=0
	__last=None
	def move(self,paras):
		self.__timer+=1
		if self.__timer%4==0:
			self.__move+=1
		while 1:
			val=random.randint(0,3)
			if val!=self.__last:
				break
		if val==0:
			self.loc[0]-=1
			if self.loc[0]<0:
				self.loc[0]=0
		elif val==1:
			self.loc[1]+=1
			if self.loc[1]>self.limit[1]-1:
				self.loc[1]=self.limit[1]-1
		elif val==2:
			self.loc[0]+=1
			if self.loc[0]>self.limit[0]-1:
				self.loc[0]=self.limit[0]-1
		elif val==3:
			self.loc[1]-=1
			if self.loc[1]<0:
				self.loc[1]=0
		self.__last=val
#		print self.loc
		return self.loc
	
def training(player,display=0):
	x=random.randint(0,15)
	y=random.randint(0,15)
	loc=[0,0]
	soldier=Player(player,[16,16],loc)
	goal=[8,12]
	trainer=Trainer(None,[16,16],goal)
	last=[None]
	moves=100
	score=0
	for move in range(moves):
		if display:
			displaygame(loc,goal,[16,16])
		dependencies=goal+[move]
		loc,val=soldier.move(dependencies)
		if val in last:
			score+=1000
		last.append(val)
		if loc==goal:
			if display:
					print "\n\nAI won!"
			score=0
			break
		last.remove(last[0])
		score+=1
	score+=distance(loc,goal)
	return score

def distance(a,b):
	mag=pow((b[0]-a[0]),2)+pow((b[1]-a[1]),2)
	return math.sqrt(mag)

def battle(p1,p2,display=0,moves=10):
	arena=[10,10]
	redloc=[random.randint(0,arena[0]-1),random.randint(0,arena[1]-1)]
	blueloc=[(redloc[0]+5)%5,(redloc[1]+2)%5]
	redlast=[None]
	bluelast=[None]
	red=Player(p1,arena,redloc)
	blue=Player(p2,arena,blueloc)
	for move in range(moves):
		if display:
			displaygame(redloc,blueloc,arena)
		reddep=blueloc+[move]
		redloc,rlast=red.move(reddep)
		if rlast in redlast:
			if display:
				print "BBBBBBBB By default BBBBBBBB"
			return 'blue'
		if redloc==blueloc:
			if display:
				print "RRRRRRRR By Capture RRRRRRRR"
			return 'redc'
		redlast.remove(redlast[0])
		redlast.append(rlast)
		bluedep=redloc+[move]
		blueloc,blast=blue.move(bluedep)
		if blast in bluelast:
			if display:
				print "RRRRRRRR By default RRRRRRR"
			return 'red'
		if blueloc==redloc:
			if display:
				print "BBBBBBBB By Capture BBBBBBB"
			return 'bluec'
		bluelast.remove(bluelast[0])
		bluelast.append(blast)
	return distance(redloc,blueloc)

def practice(popn,funct):
	val=[]
	for tree in popn:
		val.append(training(tree))
	s=zip(val,popn)
	s.sort()
	best=[]
	scores=[]
	for results in s:
		best.append(results[1])
		scores.append(results[0])
	return best,scores

def warevaluator(popn,funct,display=0):
#	print popn
	val=[0 for i in range(len(popn))]
	for i in range(len(popn)):
		for j in range(len(popn)):
			if i==j:
				continue
			res=battle(popn[i],popn[j],display,10)
			if res == 'red':
				val[j]+=100
			elif res == 'redc':
				val[j]+=100
				val[i]-=10
			elif res == 'blue':
				val[i]+=100
			elif res=='bluec':
				val[i]+=100
				val[j]-=10
			else:
				val[i]+=res
				val[j]+=res
	s=zip(val,popn)
	s.sort()
	best=[]
	scores=[]
	for results in s:
		best.append(results[1])
		scores.append(results[0])
	return best,scores


def displaygame(p1,p2,board=[3,3]):
	os.system('clear')
	for i in range(board[0]):
		for j in range(board[1]):
			if [i,j]==p1:
				print 'R',
			elif [i,j]==p2:
				print 'B',
			else:
				print '.',
		print 
	print '============================================================================'
	time.sleep(1)

class Human:
	def evaluate(self,useless):
		return input("Enter your move ")



def main():
	winners=[]
#	for i in range(10):
	nodes=defaults.nodelist
	dataset=[(0,0),(0,1),(0,2),(0,3),(1,3),(2,3),(2,2),(1,2),(1,1),(2,1),(2,0),(1,0)]
	calc=evolution.ai(3,5,nodes,None)
	popn=calc.generate_population(5)
	res,ans=calc.evolve(popn,practice,prob_mutation=0.3,prob_new=0.2,offsprings=100,maxgenerations=1000)
	print "===============Got Solution============="
	print "Best is %d \n"%res
	ans.display_tree()
#	winners.append(ans)

	fname=raw_input("Enter name of file ")
	f=open(fname,'wb')
	pickle.dump(ans,f)
	f.close()

def getwinner():
	fname=raw_input("Enter name of file ")
	f=open(fname,'rb')
	obj=pickle.load(f)
	f.close()
	return obj

if __name__=='__main__':
	main()
	

