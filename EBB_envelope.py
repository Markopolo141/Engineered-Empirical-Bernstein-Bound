import json
from math import exp, sqrt
from utils import *
import sys

print "*computing deviation of EBB bound from envelope*"
datapoints = []

# define the envelope
def envelope(a,b,n):
	return (1.0/(b-exp(-0.1*(n/4.0-n*a)**2))+100/((n/4.0-n*a)**3)-12*b+13+20*a+8000/(n**2))/(20*sqrt(n))

# define envelope bound:
def bound(a,b,n):
	return b-exp(-0.1*((0.25-a)*n)**2)>0.05

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
		if bound(a,b,n):
			# calculate the height of the envelope above the data
			v = envelope(a,b,n)-c
			# raise exception if the envelope below the data
			if v<0:
				raise Exception("envelope below the data!")
			datapoints.append(v)

# calculate the median height of the envelope above the data, and the number of datapoints
print "EBB envelope: {} above data, datapoints: {}".format(median(datapoints),len(datapoints))
