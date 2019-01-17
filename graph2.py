import json
from utils import *
import sys
from math import sqrt,log

# Maurer and Pontil's EBB
def entropy2(s,w,n):
	if w>2:
		w=2
	if w<=0:
		return float("inf")
	return sqrt(2*s*log(2/w)/n) + 7*log(2/w)/(3*(n-1))

# Hoeffdings, inverted on first argument
h = invert(hoeffding_1,argument=1)

# open files holding data for latex 2d plots
f1 = open("graph_1.tex","w")
f2 = open("graph_2.tex","w")

#shorthand for calculating percent loss from y to x
l = lambda x,y:(y-x)*100.0/y

#load all data
filename = "formatted_data.json"
print "loading data {}".format(filename)
data = []
with open("{}".format(filename), "r") as f:
	data = json.load(f)

# read arguments and load data
lenargv = len(sys.argv)-1
for ii in range(lenargv):
	n = int(sys.argv[1+ii])
	# write datums
	f1.write("\n{}:\n".format(n))
	f2.write("\n{}:\n".format(n))
	f1.write("".join([str((d[1],l(d[3],entropy2(d[1],0.5,n)))) for d in data if (d[0]==n) and (d[2]==0.5) and (0.5>sqrt(d[1])+sqrt(2*log(2.0/0.5)/(n-1)))])+'\n')
	f2.write("".join([str((d[1],l(h(d[1],0.5,n),d[3]))) for d in data if (d[0]==n) and (d[2]==0.5)])+'\n')

print "done"
#close files
f1.close()
f2.close()


