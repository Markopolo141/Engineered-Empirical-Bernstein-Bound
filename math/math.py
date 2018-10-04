from sympy import symbols, exp, simplify, diff, factor, expand
from sympy.interactive.printing import init_printing
init_printing(use_unicode=False, wrap_line=False, no_global=True)
from sympy.solvers import solve
import pdb

n,x,s,q,t = symbols("n,x,s,q,t")
def function_F(x,y):
	return (x*exp(y)+y**2*exp(-x/y))/(x+y**2)
G = 2*exp(-q*n*t)*function_F(q**2*s,q*x)**n
dG = simplify(diff(G,q))
dGs = solve(dG,q)
dGsol = simplify(G.subs({q:dGs[0]}))

def function_G(x,y):
	return 1-x+x*exp(-y)
H = exp(q*n*(s-t))*function_G(s/(x**2),q*x**2)**n
dH = simplify(diff(H,q))
dHs = solve(dH,q)
dHsol = simplify(H.subs({q:dHs[0]}))

b,d = symbols("b,d")
print "now you just need to rearrange the following:"
print "P(hat{mu}>t) < ", dGsol.subs({x:b})
print "P(s-hat{s}<t) < ", dHsol.subs({x:d})

