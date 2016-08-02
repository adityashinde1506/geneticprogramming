from gplib import *

def add(l):
	return sum(l)

l=[1,2]
addfunc=function(add,'add',len(l))
addnode=node(addfunc,l)

def sub(l):
	return l[0]-l[1]

m=[6,4]
subfunc=function(sub,'sub',len(m))
subnode=node(subfunc,m)

def mul(l):
	return l[0]*l[1]

n=[9,8]
mulfunc=function(mul,'mul',len(n))
mulnode=node(mulfunc,n)

def div(l):
	return l[0]/l[1]

o=[6,3]
divfunc=function(div,'div',len(o))
divnode=node(divfunc,o)

def isgreater(l):
	if l[0]>l[1]:
		return l[0]
	else:
		return l[1]

p=[5,4]
isgreaterfunc=function(isgreater,'is greater',len(p))
isgreaternode=node(isgreaterfunc,p)

def square(l):
	return l[0]*l[0]

q=[2]
sqrfunc=function(square,'square',len(q))
sqrnode=node(sqrfunc,q)

nodelist=[addnode,subnode,mulnode,isgreaternode,sqrnode]

	

