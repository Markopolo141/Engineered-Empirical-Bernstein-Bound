import json
from utils import *
from tqdm import tqdm
import sys
import pdb

h = invert(hoeffding_1,argument=1)

if __name__ == '__main__':
	assert len(sys.argv)==2
	print "loading data"
	with open("{}".format(sys.argv[1]), "r") as f:
		import_data = json.load(f)
	print "parsing data"
	config = import_data['config']
	D = config['D']
	halfD = D/2.0
	quarterD = D/4.0
	n = config['n']
	ddims = config['ddims']
	dims = config['dims']
	ydims = 100
	data = import_data['data']
	data = [list(eval(a))+[b] for a,b in data.iteritems()]
	
	print "trimming data"
	data = [(a,b,c,d) for a,b,c,d in data if a<=D**2*c*(1-c)]
	print "curbing data"
	data = [(a,b,c,min(d,efron(a,b,D,n),entropy(a,b,D,n))) for a,b,c,d in data]
	
	print "inverting data"
	data = [(r(a-b),d,c,r(a)) for a,b,c,d in data]
	print "interpolating data"
	data = data_interpolate(data, xxxrange(0.0,1.0,ydims), value_col=1,source_col=3,extrapolation=False,debug=True)
	print "categorzing data"
	f_data = categorize(data,[0,1,2,3])
	print "minimizing"
	
	results = []
	for s in tqdm(xxxrange(0.0,quarterD,dims)):
		for sy,y in enumerate(xxxrange(0,1.0,ydims)):
			min_array = []
			for z in xxxrange(0,y,sy):
				max_array = []
				for d in xxxrange(0.0,halfD,ddims):
					get_value = getter(f_data,[s,r(y-z),d])
					if get_value is not None:
						max_array.append((get_value,d))
				if len(max_array)>0:
					max_array2 = [D*(1-d)*h(m/(D*(1-d)*D*(1-d)),z,n) for m,d in max_array]
					min_array.append(max(max_array2))
			if len(min_array)>0:
				results.append((s,y,min(min_array)))
	
	print "outputting"
	with open("formatted_{}".format(sys.argv[1]),"w") as f:
		json.dump(results,f)
	print "done :-)"


