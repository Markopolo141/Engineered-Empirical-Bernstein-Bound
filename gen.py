
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

# display some intro info
print "processing input from {} files".format(len(sys.argv)-1)

# holding array for data between files
total_results = []

for input_index in range(1,len(sys.argv)):
	# conduct basic data import checks
	print "loading data: {}".format(sys.argv[input_index])
	with open("{}".format(sys.argv[input_index]), "r") as f:
		import_data = json.load(f)
	print "parsing data"
	config = import_data['config']
	D = config['D']
	n = config['n']
	ddims = config['ddims']
	dims = config['dims']
	data = import_data['data']
	data = [list(eval(a))+[b] for a,b in data.iteritems()]

	# reformulate the data from being a list of points to nested dictionaries of values
	print "categorzing data"
	f_data = categorize(data,[0,1,2,3])

	# conduct the main data processing - for every value of s and y (variance and offset)
	#   take the maximum with d, and then the minimum with x
	print "composing"
	results = []
	iterator = xxxrange(0.0,D*D/4.0,dims)
	if tqdm_enabled:
		iterator = tqdm(iterator)
	for s in iterator: #for every value of s
		for sy,y in enumerate(xxxrange(0,1.0,dims)): #for every value of y
			for x in xxxrange(0,y,sy): # for each value of x
				max_array = []
				for d in xxxrange(0.0,D,2*ddims): #take maximum with d d
					get_value = getter(f_data,[s,r(y-x),r(min(d,1-d))]) #check if data point of z^-1 exists at (s,y-x,d) and append it if it does
					if get_value is not None:
						max_array.append((get_value,x))
				if len(max_array)>0: #compose z^-1 data points with hoeffding's inverse (being carefull with scaling)
					max_array2 = [D*d*h(m/(D*d*D*d),x,n) for m,x in max_array]
					results.append((s,y,x,max(max_array2)))
	
	# recategorize to take the minimum x
	print "recategorizing data"
	f_results = categorize(results,[0,1,2,3])

	# take the minimum x
	print "taking minimum x"
	total_results += sum([[(n,k,kk,min(f_results[k][kk].values())) for kk in f_results[k].keys()] for k in sorted(f_results.keys())],[])
	

# output data of our new EBB
print "outputting"
with open("formatted_data.json","w") as f:
	json.dump(total_results,f)
print "done :-)"


