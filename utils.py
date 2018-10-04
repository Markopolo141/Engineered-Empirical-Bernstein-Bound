
# conduct import and checks
from math import exp,log
from copy import deepcopy as copy
try:
	from tqdm import tqdm
	tqdm_enabled=True
except ImportError:
	tqdm_enabled=False

# a cheap function to compute the median of a list of data
def median(data):
	data = sorted(data)
	return data[len(data)/2]


# Hoeffding's famous bound
def hoeffding_1(s,t,b,D,n,replacement=0):
	sox = s/(b**2)
	tox = t/b
	if sox<0 or tox<0:
		return float('nan')
	if s>b*(D-b):
		return float('nan')
	if (sox==0) and (tox==0):	
		return 1.0
	if t>b:
		return replacement
	aa = sox+tox
	a = sox/aa
	bb = 1-tox
	b = 1/bb
	e = n/(sox+1)
	aa = aa*e
	bb = bb*e
	return a**aa*b**bb

# our variance bound
def hoeffding_2(s,t,d,D,n,replacement=0):
	sox = s/(d**2)
	tox = t/(d**2)
	if sox<0 or tox<0:
		return float('nan')
	if sox>1:
		return 0.0
	if sox-tox<=0:
		return replacement
	if s>d*(D-d):
		return replacement
	A = 1-sox
	B = 1+tox-sox
	C = sox
	D = sox-tox
	E = (A/B)**B*(C/D)**D
	return E**n
	

# a function wrapper that numerically returns its inverts it on the indexed argument
def invert(f,argument=0,lower_bound=0,upper_bound=100,start_power=1,max_power=10,upper_bound_return=None):
	def inner(*args):
		args2 = list(copy(args))
		vv = args[argument]
		x = lower_bound
		args2[argument]=x
		v1 = f(*args2)
		i=start_power
		while i<max_power:
			x2 = x+pow(2,-float(i))
			args2[argument]=x2
			v2 = f(*args2)
			if (v1 is None) or ((v2-v1)*(vv-v1)>=0 and vv!=v1 and (v2-v1)/(vv-v1)<=1):
				if x2>upper_bound:
					return upper_bound_return
				x = x2
				v1 = v2
			else:
				i += 1
		return x
	return inner

# an iterator function, that returns a list of 'steps' numbers between start and stop
def xxxrange(start,stop,steps):
	assert steps>=0
	if steps==0:
		return [start]
	a = []
	for i in range(steps+1):
		a.append( (stop-start)*((i*1.0)/steps)+start )
	return a



def xxrange(start, stop, step=1.0, proportional=False):
	assert step != 0
	if start==stop:
		return [start]
	direction = 1 if stop>start else -1
	if direction*step<0:
		step *= -1
	if proportional:
		step *= abs(stop-start)
	a = []
	i = 0
	z = start*direction
	while (z <= stop*direction):
		a.append(z*direction)
		i += 1
		z = (start+i*step)*direction
	return a


