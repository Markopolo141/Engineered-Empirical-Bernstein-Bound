from math import exp


def xxrange(start,stop,step):
	x = start
	while x<stop:
		yield x
		x += step

def f(k,g):
	if (k-g==0):
		return 0
	return exp((k-g)**2*1.0/8) - (k*exp(g)-g*exp(k))/(k-g)

for x in xxrange(-10,10,0.005):
	for y in xxrange(-10,10,0.005):
		#print f(x,y)
		if f(x,y)<0:
			print "whoa"
