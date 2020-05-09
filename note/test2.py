import numpy as np
import matplotlib.pyplot as plt
from math import factorial, floor

def xxrange(start,stop,step):
	x = start
	while (x<stop):
		yield x
		x += step

def ncr(n,r):
	return factorial(n)/(factorial(n-r)*factorial(r))

hatmu = 0.7
t=0.01
mu=hatmu+t
n = 9


import pdb
pdb.set_trace()

cutoff = 1-n*(1-hatmu)/(n-floor(hatmu*n))
alpha_cutoff = (mu-1)*1.0/(cutoff-1)
cutoff_probability = 0
for nn in range(0,int(floor(hatmu*n))+1):
	cutoff_probability += ncr(n,nn)*alpha_cutoff**(n-nn)*(1-alpha_cutoff)**(nn)

cutoff = (n*hatmu-1)/(n-1)
print cutoff

xvalues = []
values = []
values2 = []

for x in list(xxrange(0,hatmu,0.001)):
	alpha = (mu-1)/(x-1)
	p = 0
	for nn in range(0,n+1):
		if (nn*x+(n-nn)<=n*hatmu):
			p += ncr(n,nn)*alpha**nn*(1-alpha)**(n-nn)
	values.append(p)
	xvalues.append(x)
	if (x>cutoff):
		values2.append(cutoff_probability)
	else:
		values2.append(0.0)


x = np.array(xvalues)
y = np.array(values)
y2 = np.array(values2)


#x = np.linspace(0, 10, 500)
#y = np.sin(x)

fig, ax = plt.subplots()

line2, = ax.plot(x, y)
line2, = ax.plot(x, y2)


ax.legend()
plt.show()

