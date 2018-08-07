from sympy import symbols, exp, simplify, diff, factor, expand, Sum, Rational,sqrt,log
from sympy.interactive.printing import init_printing
init_printing(use_unicode=False, wrap_line=False, no_global=True)
from sympy.matrices import Matrix
from sympy.solvers import solve
#from sympy.abc import x
from sympy.core import Add, Mul
from tqdm import tqdm
from random import random
import pdb

def prod(a):
	b = 1
	for aa in a:
		b *= aa
	return b
def fac(n):
	return prod(list(range(1,n+1)))
def xxrange(start, stop, step=1.0):
	assert step>0
	a = []
	i = 0
	z = start
	while (z <= stop):
		a.append(z)
		i += 1
		z = start+i*step
	return a


a,n,x,s,q,t,y,r,b,d = symbols("a,n,x,s,q,t,y,r,b,d")
a,z = symbols("a,z")
def function_F(x,y):
	return (x*exp(y)+y**2*exp(-x/y))/(x+y**2)
G = exp(-q*t)*function_F(q**2*s,q*x)
dG = factor(simplify(expand(diff(G,q))))
dGs = solve(dG,q)
dGsol = simplify(expand(G.subs({q:dGs[0]})))
pdb.set_trace()

'''err=0
for ss in tqdm(xxrange(0.1,3,0.3)):
	for tt in xxrange(0.1,3,0.3):
		for xx in xxrange(tt+0.1,tt+4,0.3):
			A= (dGsol- ((s+t*x)/s)**((-s-t*x)/(s+x**2))*(x/(x-t))**((x**2-t*x)/(s+x**2)) ).evalf(subs={s:ss,x:xx,t:tt})
			err += (A*A.conjugate()).evalf()
print err'''

H = exp(q*(s-y))*(x**2+s*exp(-q*x**2)-s)/x**2
dH = factor(simplify(expand(diff(H,q))))
dHs = solve(dH,q)
dHsol = simplify(expand(H.subs({q:dHs[1]})))

'''err=0
temp_expr = simplify(exp(dHs[1]*x**2))
print temp_expr
for ss in tqdm(xxrange(0.1,3,0.3)):
	ss += random()
	for yy in xxrange(0.1,3,0.3):
		ss += random()
		for xx in xxrange(yy+0.1,yy+4,0.3):
			if temp_expr.evalf(subs={s:ss,x:xx,y:yy}) > 0:
				A= (dHsol- ((x**2-s)/(x**2+y-s))**((x**2+y-s)/x**2)*((s-y)/s)**((y-s)/x**2) ).evalf(subs={s:ss,x:xx,y:yy})
				err += (A*A.conjugate()).evalf()
print err'''

J = (exp(q*(-t-x/2))+exp(q*(-t+x/2)))/2
dJ = factor(simplify(expand(diff(J,q))))
dJs = solve(dJ,q)
dJsol = simplify(expand(J.subs({q:dJs[0]})))

'''err=0
for xx in tqdm(xxrange(0.1,3,0.3)):
	xx += random()
	for tt in xxrange(0.1,xx/2.01,0.3):
		A= (dJsol- ((x-2*t)/(x+2*t))**((2*t+1)/(2*x))*(x/(x-2*t)) ).evalf(subs={x:xx,t:tt})
		err += (A*A.conjugate()).evalf()
print err'''


K = (b*exp(q*a)-a*exp(q*b))/((b-a)*exp(q*t))
dK = factor(simplify(expand(diff(K,q))))
dKs = solve(dK,q)
dKsol = simplify(expand(J.subs({q:dKs[0]})))

G = dGsol
H = dHsol
J = dJsol
#G = (((s+t*x)/s)**((-s-t*x)/(s+x**2))*(x/(x-t))**((x**2-t*x)/(s+x**2)))
#H = (((x**2-s)/(x**2+y-s))**((x**2+y-s)/x**2)*((s-y)/s)**((y-s)/x**2))
#J = ((x-2*t)/(x+2*t))**((2*t+1)/(2*x))*(x/(x-2*t))
master = 2*G**n + H**n
print master


