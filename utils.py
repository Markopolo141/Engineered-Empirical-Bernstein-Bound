
# conduct import and checks
from math import exp,log
from copy import deepcopy as copy
try:
	from tqdm import tqdm
	tqdm_enabled=True
except ImportError:
	tqdm_enabled=False

# convert a list of points into nested set of dictionaries in order of indices
def categorize(data,indices):
	if len(indices)==1:
		return min([d[indices[0]] for d in data])
	d = {}
	for data_item in data:
		data_item_index = data_item[indices[0]]
		d[data_item_index] = d.get(data_item_index,[]) + [data_item]
	for dd in d.keys():
		d[dd] = categorize(d[dd],indices[1:])
	return d

# convert a nested set of dictionaries into a list of points (reverse of categorize)
def decategorize(data):
	if isinstance(data,dict):
		r = []
		for k in data.keys():
			for kk in decategorize(data[k]):
				r.append([k]+kk)
		return r
	return [[data]]

# for a nested set of dictionaries d, attempt to get the entery associated with sequential keys
def getter(d, keys):
	dd = d
	for k in keys:
		dd = dd.get(k,None)
		if dd is None:
			return dd
	return dd

# returns one if denominator is zero
def protected_div(a,b):
	if b!=0:
		return a/b
	else:
		return 1

# Maurer and Pontil's entropy variance bound
def entropy(s,t,d,n):
	if s>d/4.0 or s<0:
		raise Exception
	if t<0:
		return 1.0
	if t>1 or t>s:
		return 0.0
	return min(1.0,exp(protected_div(-(n-1)*t**2, 2*s*d**2)))

# Hoeffding's famous bound
def hoeffding_1(sox,tox,n,replacement=0):
	if sox<0 or tox<0:
		return float('nan')
	if sox+tox==0:	
		return 1.0
	if tox>=1:
		return replacement
	aa = (sox+tox)/(sox+1)
	a = sox/(sox+tox)
	bb = (1-tox)/(sox+1)
	b = 1/(1-tox)
	return (a**aa*b**bb)**n


# a function wrapper that numerically returns its inverts it on the indexed argument
def invert(f,argument=0,lower_bound=0,upper_bound=100,start_power=1,upper_bound_return=None):
	def inner(*args):
		args2 = list(copy(args))
		vv = args[argument]
		x = lower_bound
		args2[argument]=x
		v1 = f(*args2)
		i=start_power
		while i<15:
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

# conducts a basic rounding
def r(a):
	b = 100000
	a = round(a*b)*1.0/b
	return a

# an iterator function, that returns a list of 'steps' numbers between start and stop
def xxxrange(start,stop,steps):
	assert steps>=0
	if steps==0:
		return [start]
	a = []
	for i in range(steps+1):
		a.append( (stop-start)*((i*1.0)/steps) )
	return a


