import json
from utils import *
import sys

print "*computing deviation of EBB bound from envelope*"
datapoints = []

# for each of the data files inputted
lenargv = (len(sys.argv)-1)/2
for ii in range(lenargv):
	# load and parse the json values and n parameters
	filename = sys.argv[ii*2+1]
	n = int(sys.argv[ii*2+2])
	print "loading data {}".format(filename)
	data = []
	with open("{}".format(filename), "r") as f:
		data = json.load(f)
	data = [d for i,d in enumerate(data)]

	# for each of the data values in range
	for a,b,c in data:
		if b-exp(-((0.25-a)*n)**2)>0.15:
			# calculate the height of the envelope above the data
			v = (0.75 - 0.5*b + 0.25/((0.25-a)*n) + 0.05/(b-exp(-((0.25-a)*n)**2)))/sqrt(n)-c
			# raise exception if the envelope below the data
			if v<0:
				raise Exception("envelope below the data!")
			datapoints.append(v)

# calculate the median height of the envelope above the data, and the number of datapoints
from statistics import median
print "EBB envelope: {} above data, datapoints: {}".format(median(datapoints),len(datapoints))
