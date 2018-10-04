
# Conduct all nessisary imports
import json
from utils import *
import sys
try:
	from tqdm import tqdm
	tqdm_enabled=True
except ImportError:
	tqdm_enabled=False

# create inverted hoeffdings bound on the second argument
h = invert(hoeffding_1,argument=1)

# conduct basic data import checks and parse nessisary data
assert len(sys.argv)==3
print "loading data: {}".format(sys.argv[1])
with open("{}".format(sys.argv[1]), "r") as f:
	import_data = json.load(f)
print "parsing data"
config = import_data['config']
D = config['D']
n = int(sys.argv[2])
ddims = config['ddims']
dims = config['dims']
data = import_data['data']
data = [list(eval(a))+[b] for a,b in data.iteritems()]

# set the number of interpolation points
ydims = 100

# take the minimum of our bound and Maurer and Pontil's entropy bound
#print "curbing data"
#data = [(a,b,c,min(d,entropy(a,b,D,n))) for a,b,c,d in data]

# conduct all coordinate swapping to create function z^-1
print "inverting data"
data = [(r(a-b),pow(d,n),c,r(a)) for a,b,c,d in data]

# interpolate function z^-1 to create evenly spaced values on the second index
print "interpolating data"
data = data_interpolate(data, xxxrange(0.0,1.0,ydims), value_col=1,source_col=3,extrapolation=False,debug=True)

# reformulate the data from being a list of points to nested dictionaries of values
print "categorzing data"
f_data = categorize(data,[0,1,2,3])

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


