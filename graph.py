
import json
from utils import *

filename = "data200_50_50"
n=200
D=1.0

print "loading data"
with open("{}.json".format(filename), "r") as f:
	import_data = json.load(f)

data = import_data['data']
results = [list(eval(a))+[b] for a,b in data.iteritems()]
print "trimming data"
results = [(a,b,c,d) for a,b,c,d in results if a<=D*c*(1-c)]
print "recategorzing data"
results = categorize(results,[0,1,2,3])
print "maximizing"
for a in results.keys():
	for b in results[a].keys():
		results[a][b] = max(results[a][b].values())

print "generating graph"
K1 = sorted(results.keys())
s = ""


for i,k1 in enumerate(K1[:-1]):
	K2 = sorted(results[K1[i+1]].keys())
	for o,k2 in enumerate(K2[:-1]):
		if o>0:
			s += "{} {} {}\n".format(K1[i],K2[o],		entropy(K1[i],K2[o],D,n) - results[K1[i]][K2[o]])
			s += "{} {} {}\n".format(K1[i+1],K2[o],		entropy(K1[i+1],K2[o],D,n) - results[K1[i+1]][K2[o]])
			s += "{} {} {}\n".format(K1[i],K2[o-1],		entropy(K1[i],K2[o-1],D,n) - results[K1[i]][K2[o-1]])
		s += "\n"
		s += "{} {} {}\n".format(K1[i],K2[o],		entropy(K1[i],K2[o],D,n) - results[K1[i]][K2[o]])
		s += "{} {} {}\n".format(K1[i+1],K2[o],		entropy(K1[i+1],K2[o],D,n) - results[K1[i+1]][K2[o]])
		s += "{} {} {}\n".format(K1[i+1],K2[o+1],	entropy(K1[i+1],K2[o+1],D,n) - results[K1[i+1]][K2[o+1]])
with open("{}_graph.dat".format(filename),"w") as f:
	f.write(s)


print "done :-)"
