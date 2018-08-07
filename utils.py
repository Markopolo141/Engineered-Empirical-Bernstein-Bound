from math import exp,sqrt,log
from copy import deepcopy as copy
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from tqdm import tqdm
import pdb

def destringify(data):
	if isinstance(data,dict):
		for k in data.keys():
			data[float(k)] = destringify(data[k])
			data.pop(k)
		return data
	return data

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

def decategorize(data):
	if isinstance(data,dict):
		r = []
		for k in data.keys():
			for kk in decategorize(data[k]):
				r.append([k]+kk)
		return r
	return [[data]]

def getter(d, keys):
	dd = d
	for k in keys:
		dd = dd.get(k,None)
		if dd is None:
			return dd
	return dd

def interpolate(dataxy, yval,min_points=2,extrapolation=True,high_ordering=True):
	if len(dataxy)<min_points:
		return None
	index1 = 0
	index2 = 1
	value1 = dataxy[0][1] - yval
	value2 = dataxy[1][1] - yval
	if value1<value2:
		value1,index1,value2,index2 = value2,index2,value1,index1
	if value1==0 and value2==0:
		if high_ordering:
			zero_index = max(index1,index2)
		else:
			zero_index = min(index1,index2)
	elif value1==0:
		zero_index = index1
	elif value2==0:
		zero_index = index2
	else:
		zero_index = -1
	zero_value = None if zero_index==-1 else dataxy[zero_index][0]
	for i in range(2,len(dataxy)):
		dxy = dataxy[i]
		v = dxy[1] - yval
		if zero_index < 0:
			if v>0:
				if value1<0:
					value1,index1,value2,index2 = v,i,value1,index1
				elif v<value1:
					value1,index1 = v,i
				else:
					continue
			elif v<0:
				if value2>0:
					value1,index1,value2,index2 = value2,index2,v,i
				elif v>value2:
					value2,index2 = v,i
				else:
					continue
			elif v==0:
				zero_index = i
				zero_value = dxy[0]
				continue
			if value1<value2:
				value1,index1,value2,index2 = value2,index2,value1,index1
		elif v==0:
			if (high_ordering and dxy[0]>zero_value) or ((not high_ordering) and dxy[0]<zero_value):
				zero_index = i
				zero_value = dxy[0]
	if zero_index>=0:
		return zero_value,yval
	if (extrapolation is not True) and (value2*value1>0):
		return None
	p2 = dataxy[index1]
	p1 = dataxy[index2]
	if p2[1]-p1[1] !=0:
		f = (yval-p1[1])/(p2[1]-p1[1])
		return f*(p2[0]-p1[0]) + p1[0],yval
	else:
		return (p2[0]+p1[0])*1.0/2,yval


def data_interpolate(data, values, value_col=1,source_col=0,min_points=2,extrapolation=True,high_ordering=True,debug=False,kulling_singles=True):
	assert len(data)>0
	assert value_col!=source_col
	coord_cols = list(range(len(data[0])))
	coord_cols.pop(max(value_col,source_col))
	coord_cols.pop(min(value_col,source_col))
	coord_pairs = [[] for i in range(len(coord_cols))] if len(coord_cols)>0 else None
	coord_points = []
	coord_point_insertion_index = 0
	if debug:
		print " -segregating data:"
		iterator = tqdm(data)
	else:
		iterator = data
	for d in iterator:
		temp_coord_indices = [True for i in range(len(coord_points))]
		has_match = len(coord_points)>0
		for ii,i in enumerate(coord_cols):
			temp_coord_indices2 = []
			has_match = False
			for tt,t in enumerate(temp_coord_indices):
				match = (t and (d[i]==coord_pairs[ii][tt]))
				temp_coord_indices2.append(match)
				has_match = match or has_match
				if match:
					coord_point_insertion_index = tt
			temp_coord_indices = temp_coord_indices2
			if not has_match:
				break
		if has_match:
			coord_points[coord_point_insertion_index].append((d[source_col],d[value_col]))
		else:
			coord_points.append([(d[source_col],d[value_col])])
			for ii,i in enumerate(coord_cols):
				coord_pairs[ii].append(d[i])
	new_coord_points = []
	if debug:
		print " -interpolating segregated data:"
		iterator = tqdm(coord_points)
	else:
		iterator = coord_points
	for c in iterator:
		n = []
		for v in values:
			nn = interpolate(c,v,min_points=min_points,extrapolation=extrapolation,high_ordering=high_ordering)
			if nn is not None:
				n.append(nn)
		new_coord_points.append(n)
	coord_pairs = zip(*coord_pairs) if coord_pairs is not None else [[]]
	new_data = []
	if debug:
		print " -desegregating data:"
		iterator = tqdm(enumerate(coord_pairs))
	else:
		iterator = enumerate(coord_pairs)
	for i,c in iterator:
		if (not kulling_singles) or len(new_coord_points[i])>1:
			for cp in new_coord_points[i]:
				a = list(c)
				if source_col<value_col:
					a.insert(source_col,cp[0])
					a.insert(value_col,cp[1])
				else:
					a.insert(value_col,cp[1])
					a.insert(source_col,cp[0])
				new_data.append(a)
	return new_data


def protected_div(a,b):
	if b!=0:
		return a/b
	else:
		return 1


def efron(s,t,d,n):
	return protected_div(d**4/(12*n) + (5-n)*s**2/(n*(n-1)), t**2)

def entropy(s,t,d,n):
	if s>d/4.0 or s<0:
		raise Exception
	if t<0:
		return 1.0
	if t>1 or t>s:
		return 0.0
	return min(1.0,exp(protected_div(-(n-1)*t**2, 2*s*d**2)))

def entropy2(s,w,n):
	if w>2:
		w=2
	if w<=0:
		return float("inf")
	return sqrt(2*s*log(2/w)/n) + 7*log(2/w)/(3*(n-1))

def entropy3(s,w,n):
	if w>2:
		w=2
	if w<=0:
		return float("inf")
	return sqrt(2*s*log(2/w)/n) + log(2/w)*(2/sqrt(n*n-1)+1/(3*n))

def entropy4(s,w,n):
	if w>2:
		w=2
	if w<=0:
		return float("inf")
	l = log(2/w)
	return (sqrt(s+l/(2*(n-1)))+sqrt(l/(2*(n-1))))*sqrt(2*l/n)+l/(3*n)

def hoeffding_0(tox,n):
	return exp(-2*tox**2*n)

def hoeffding_1(sox,tox,n,replacement=0):
	if sox<0 or tox<0:
		return float('nan')
	if sox+tox==0:	
		return 1.0
	if tox>=1:
		return replacement
	aa = sox+tox
	a = sox/aa
	bb = 1-tox
	b = 1/bb
	e = n/(sox+1)
	aa = aa*e
	bb = bb*e
	return a**aa*b**bb


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


def plot(data,xaxis=None,yaxis=None,zaxis=None):
	fig = plt.figure()
	ax = fig.gca(projection='3d')
	x = [a[0] for a in data]
	y = [a[1] for a in data]
	z = [a[2] for a in data]
	if xaxis is not None:
		ax.set_xlabel(xaxis)
	if yaxis is not None:
		ax.set_ylabel(yaxis)
	if zaxis is not None:
		ax.set_zlabel(zaxis)
	ax.scatter(x, y, z,s=2.7)
	plt.show()




def r(a):
	b = 100000
	a = round(a*b)*1.0/b
	return a

def xxxrange(start,stop,steps):
	assert steps>=0
	if steps==0:
		return [start]
	a = []
	for i in range(steps+1):
		a.append( (stop-start)*((i*1.0)/steps) )
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

