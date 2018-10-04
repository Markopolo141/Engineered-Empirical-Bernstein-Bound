
# Conduct all nessisary imports
import json
from utils import *
import sys
import pdb
try:
	from tqdm import tqdm
	tqdm_enabled=True
except ImportError:
	tqdm_enabled=False




from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt


small=1e-7
max_power = 15

# create inverted hoeffdings bound on the second argument
h1 = invert(hoeffding_1,argument=1,upper_bound=10,max_power=max_power)
h2 = invert(hoeffding_2,argument=1,upper_bound=10,max_power=max_power)
def mh2(s,y,d,D,n):
	if s>d*(D-d):
		return None
	valh2 = h2(s,y,d,D,n)
	if (valh2 is not None):
		return s-valh2
	else:
		return 0.0
def invert_mh2(s,y,d,D,n):
	#if s>d*(D-d):
	#	return None
	mins = small
	maxs = d*(D-d)
	minsv = mh2(mins,y,d,D,n)
	maxsv = mh2(maxs,y,d,D,n)
	if (s<minsv):
		return None
	if (s>maxsv):
		return d*(D-d)
	for i in range(max_power):
		mids = (mins+maxs)/2.0
		midsv = mh2(mids,y,d,D,n)
		if s<midsv:
			maxs = mids
			maxsv = midsv
		else:
			mins = mids
			minsv = midsv
	return mids
def ebb(s,y,D,n,dims,ddims):
	minv = float("inf")
	for phi in xxxrange(0.0,1.0,dims):
		maxv = 0
		for b in xxxrange(1.0/ddims,D-1.0/ddims,ddims-1):
			mm = invert_mh2(s,y*phi,max(b,D-b),D,n)
			if mm is not None:
				mm = h1(mm,y*(1.0-phi),b,D,n)
				if mm>maxv:
					maxv=mm
		if maxv<minv:
			minv=maxv
	return minv
			


fig = plt.figure()
ax = fig.gca(projection='3d')
'''xx = []
yy = []
zz = []
for s in xxrange(0,0.5,0.01):
	for y in xxrange(0.02,1.0,0.02):
		ggg = mh2(s,y,0.85,1.0,20)
		if ggg is not None:
			xx.append(s)
			yy.append(y)
			zz.append(ggg)
ax.scatter(xx, yy, zz,s=2.7,c='b')
xx = []
yy = []
zz = []
for s in xxrange(0,0.5,0.01):
	for y in xxrange(0,1.0,0.02):
		ggg = invert_mh2(s,y,0.85,1.0,20)
		if ggg is not None:
			xx.append(s)
			yy.append(y)
			zz.append(ggg)
ax.scatter(xx, yy, zz,s=2.7,c='g')'''

xx = []
yy = []
zz = []
for s in tqdm(xxrange(0,0.25,0.01)):
	for y in xxrange(0,1.0,0.02):
		ggg = ebb(s,y,1.0,20,10,10)
		if ggg is not None:
			xx.append(s)
			yy.append(y)
			zz.append(ggg)
ax.scatter(xx, yy, zz,s=2.7,c='r')
plt.show()
pdb.set_trace()

# conduct basic data import checks and parse nessisary data
assert len(sys.argv)==4
print "parsing data"
d = int(sys.argv[1])
D = int(sys.argv[2])
n = int(sys.argv[3])


# conduct the main data processing - for every value of s and y (variance and offset)
#   take the maximum with d, and then the minimum with x
print "composing"
results = []
iterator = xxxrange(0.0,D/4.0,dims)
if tqdm_enabled:
	iterator = tqdm(iterator)
for s in iterator: #for every value of s
	for sy,y in enumerate(xxxrange(0,1.0,ydims)): #for every value of y
		min_array = []
		for x in xxxrange(0,y,sy): #take the minimum with x
			max_array = []
			for d in xxxrange(0.0,D/2.0,ddims): #take the maximum with d
				get_value = getter(f_data,[s,r(y-x),d]) #check if data point of z^-1 exists at (s,y-x,d) and append it if it does
				if get_value is not None:
					max_array.append((get_value,d))
			if len(max_array)>0: #compose z^-1 data points with hoeffding's inverse (being carefull with scaling)
				max_array2 = [D*(1-d)*h(m/(D*(1-d)*D*(1-d)),x,n) for m,d in max_array]
				min_array.append(max(max_array2))
		if len(min_array)>0:
			results.append((s,y,min(min_array)))

# output data of our new EBB
print "outputting"
with open("formatted_data{}_{}_{}.json".format(n,dims,ddims),"w") as f:
	json.dump(results,f)
print "done :-)"


