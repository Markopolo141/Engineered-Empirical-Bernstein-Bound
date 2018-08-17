import json
from utils import *
from math import sqrt
import sys

print "*computing deviation of variance bound from envelope*"
datapoints = []

# define the envelope
def envelope(a,b,n):
	return (0.12+0.3*log(1.0/b)+25*b*a*a*(1-4*a)+1.5/n)/sqrt(n)

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
	for a in data.keys():
		for b in data[a].keys():
			data[a][b] = max(data[a][b].values())
	# reformulate the data from being a nested dictionaries of values to a list of points
	print "decategorzing data"
	data = decategorize(data)
	
	# invert function on the second argument
	print "inverting data"
	data = [(a,c,b) for a,b,c in data]

	# trim of the redundant upper bound 1 values
	print "trimming redundant 1s"
	data = [d for d in data if d[-1]<1.0]
	
	# calculate the height of the envelope above the data
	print "calculating"
	data = [envelope(a,b,n)-c for a,b,c in data if b>0]

	# raise exception if the envelope below the data
	for d in data:
		if d<0:
			raise Exception("envelope below the data!")
		datapoints.append(d)

# calculate the median height of the envelope above the data, and the number of datapoints
print "variance envelope: {} above data, datapoints: {}".format(median(datapoints),len(datapoints))
