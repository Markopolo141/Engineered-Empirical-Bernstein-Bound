import json
from utils import *
import sys
import random

fig = plt.figure()
ax = fig.gca(projection='3d')

lenargv = len(sys.argv)-1
for ii in range(lenargv):
	filename = sys.argv[ii+1]
	print "loading data {}".format(filename)
	data = []
	with open("{}".format(filename), "r") as f:
		data = json.load(f)
	x = [a[0] for a in data]
	y = [a[1] for a in data]
	z = [a[2] for a in data]
	ax.scatter(x, y, z,s=2.7, c=['b', 'g', 'r', 'c', 'm', 'y', 'k'][ii])

ax.set_xlabel("$\hat{\sigma}^2$")
ax.set_ylabel("y")
plt.show()

