from random import betavariate, random, randint
from math import sqrt,log
try:
	from tqdm import tqdm
	tqdm_enabled=True
except ImportError:
	tqdm_enabled=False
import sys
import json

def average(a):
	return sum(a)/len(a)

def Hoeffding_selection(m,v,n,t):
	vector = [m[i]+sqrt(log(1.0/t)/(2*n[i])) for i in range(len(m))]
	return vector.index(max(vector))

def Audibert_selection(m,v,n,t):
	vector = [m[i] + sqrt(v[i]*log(3.0/t)/(2*n[i])) + 3*log(3.0/t)/(2*n[i]) for i in range(len(m))]
	return vector.index(max(vector))

def Maurer_selection(m,v,n,t):
	vector = [m[i] + sqrt(2*v[i]*log(2.0/t)/(n[i])) + 7*log(2.0/t)/(3*(n[i]-1)) for i in range(len(m))]
	return vector.index(max(vector))

def Burgess_selection(m,v,n,t):
	v = [v[i]*n[i]*1.0/(n[i]-1) for i in range(len(m))]
	vector = []
	for i in range(len(m)):
		a = 1.0
		if n[i]*(1-v[i])>1:
			a = min(a, m[i] + (1.0/sqrt(n[i]))*((3.0/5)*sqrt(min(1.0,v[i]+25.0/n[i]))+(1.0/log(n[i]*(1-v[i])))**4))
		a = min(a, m[i]+sqrt(2*log(1.0/t)/n[i]))
		vector.append(a)
	return vector.index(max(vector))

def Random_selection(m,v,n,t):
	return randint(0,len(m)-1)




def test_method(method,N,a,b,T,t):
	s = [0.0 for i in range(N)]
	s2 = [0.0 for i in range(N)]
	n = [0.0 for i in range(N)]
	rewards = []
	for select in range(N):
		for ii in range(2):
			n[select] += 1
			v = betavariate(a[select],b[select])
			rewards.append(v)
			s[select] += v
			s2[select] += v**2
	for i in range(T-2*N):
		select = randint(0,N-1)
		m = [s[i]*1.0/n[i] for i in range(N)]
		v = [abs(s2[i]*1.0/n[i]-m[i]**2) for i in range(N)]
		#try:
		select = method(m,v,n,t)
		#except:
		#	pass
		n[select] += 1
		v = betavariate(a[select],b[select])
		rewards.append(v)
		s[select] += v
		s2[select] += v**2
	return average(rewards)

def super_test_method(method,N,a,b,T,t,TT):
	rewards = [test_method(method,N,a,b,T,t) for tt in range(TT)]
	return average(rewards)

def average_regret(N,T,t,TT):
	a = [random()*3 for i in range(N)]
	b = [random()*3 for i in range(N)]
	max_mean = max([a[i]/(a[i]+b[i]) for i in range(N)])
	return [max_mean-super_test_method(method,N,a,b,T,t,TT) for method in [Random_selection,Maurer_selection,Hoeffding_selection,Audibert_selection,Burgess_selection]]

N = 8#randint(5,12)
T = 250
t=0.5


data = []
for arg in sys.argv[1:]:
	T = int(arg)
	print "compiling T={}".format(T)

	regrets = []
	try:
		iterator = None
		if tqdm_enabled:
			for i in tqdm(range(10000)):
				regrets.append(average_regret(N,T,t,10))
		else:
			for i in range(10000):
				regrets.append(average_regret(N,T,t,10))
	except KeyboardInterrupt as e:
		pass
	data.append( [T]+[average([r[i] for r in regrets]) for i in range(len(regrets[0]))] )
with open("bandit_output.json","w") as f:
	json.dump(data,f)


