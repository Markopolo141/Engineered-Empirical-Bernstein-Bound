import json
from utils import *
import sys

print "*computing deviation of variance bound from envelope*"
datapoints = []

# for each of the data files inputted
lenargv = len(sys.argv)-1
for ii in range(lenargv):
	filename = sys.argv[ii+1]
	# load and parse the json values and parse parameters
	print "loading data - {}".format(filename)
	with open("{}".format(filename), "r") as f:
		data = json.load(f)
	n = data['config']['n']
	D = data['config']['D']
	data = [list(eval(k))+[v] for k,v in data['data'].iteritems()]

	# reformulate the data from being a list of points to nested dictionaries of values
	print "categorzing data"
	data = categorize(data,[0,1,2,3])

	# take the maximum with d
	print "maximizing"
	for a in tqdm(data.keys()):
		for b in data[a].keys():
			data[a][b] = max(data[a][b].values())
	# reformulate the data from being a nested dictionaries of values to a list of points
	print "decategorzing data"
	data = decategorize(data)

	# trim of the redundant upper bound 1 values
	data = [d for d in data if d[-1]<1.0]
	
	# calculate the height of the envelope above the data
	data = [((0.09+0.3*log(1.0/b)+25*b*a*a*(1-4*a)+1.5/n)/sqrt(n)-c) for a,b,c in data if b!=0 and c!=0]

	# raise exception if the envelope below the data
	for d in data:
		if d[-1]<0:
			raise Exception("envelope below the data!")
		datapoints.append(d[-1])

# calculate the median height of the envelope above the data, and the number of datapoints
from statistics import median
print "variance envelope: {} above data, datapoints: {}".format(median(datapoints),len(datapoints))
