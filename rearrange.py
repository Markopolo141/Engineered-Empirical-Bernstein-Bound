import json
import pdb

data = []
with open("bandit_output.json",'r') as f:
	data = json.load(f)

with open("bandit_output.tex","w") as f:
	for i in range(1,len(data[0])):
		for d in data:
			print "({}, {})".format(d[0],d[i]),
			f.write("({}, {})".format(d[0],d[i]))
		print ""
		f.write("\n\n")

