import numpy as np
from math import factorial, floor

def xxrange(start,stop,step):
	x = start
	while (x<stop):
		yield x
		x += step

def ncr(n,r):
	return factorial(n)/(factorial(n-r)*factorial(r))




def max_probability(hatmu,n,t):
	mu=hatmu+t
	cutoff = 1-n*(1-hatmu)/(n-floor(hatmu*n))
	alpha_cutoff = (mu-1)*1.0/(cutoff-1)
	cutoff_probability = 0
	for nn in range(0,int(floor(hatmu*n))+1):
		cutoff_probability += ncr(n,nn)*alpha_cutoff**(n-nn)*(1-alpha_cutoff)**(nn)
	return cutoff_probability

def max_probability2(hatmu,n,t):
	mu=hatmu+t
	alpha = (mu-1)/(hatmu-1)
	return alpha**n


hatmu = 0.85
n = 9

for t in xxrange(0,1-hatmu,0.01):
	print (t,max(max_probability(hatmu,n,t),max_probability2(hatmu,n,t))),


