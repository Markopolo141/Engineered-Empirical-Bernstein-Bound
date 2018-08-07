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


x0,xb,xa,s,y,q = symbols('x0, xb, xa, s, y, q')

# finding parabola (ax**2+bx+c) over exp(-x**2) for all xa<x<xb that minimises s*a+c
def f(x):
	return exp(-q*x**2)

m = Matrix([[xb*xb,xb,1],[x0*x0,x0,1],[2*x0,1,0]])
v = Matrix([[f(xb)],[f(x0)],[diff(f(x0),x0)]])
abc = factor(m.inv()*v)

pdb.set_trace()

# forx0 is height of the parabola above f(xa)
forx0 = simplify(abc[0]*xa**2 + abc[1]*xa + abc[2]-f(xa))*(x0-xb)**2
forx0 = (xa-xb)*(2*q*x0*(x0-xa)*(x0-xb)+2*x0-xa-xb)*exp(-q*x0**2)+(x0-xa)**2*exp(-q*xb**2)-(x0-xb)**2*exp(-q*xa**2)

# for xa and x0 scaled to have magnitude less than xb
forx0 = simplify(forx0.subs({xa:-xa*xb, x0:-x0*xb})/xb**2)
forx0 = (xa+1)*(2*q*x0*xb**2*(x0+1)*(x0-xa)+2*x0-xa+1)*exp(-q*x0**2*xb**2)-(x0+1)**2*exp(-q*xa**2*xb**2)+(x0-xa)**2*exp(-q*xb**2)

# scale with proportion to sqrt(q)
forx0 = simplify(forx0.subs({xb:xb/sqrt(q)}))
forx0 = (xa+1)*(2*x0*xb**2*(x0+1)*(x0-xa)+2*x0-xa+1)*exp(-x0**2*xb**2)-(x0+1)**2*exp(-xa**2*xb**2)+(x0-xa)**2*exp(-xb**2)

# objective function is exp(q*(s-y))*(s*a+c)
obj = simplify(exp(q*(s-y))*(s*abc[0] + abc[2]))
# obj = (((s+x0*xb)*(2*q*x0*xb-2*q*x0**2-1)+xb*(xb-x0))*exp(-q*x0**2)+(s+x0**2)*exp(-q*xb**2))*exp(q*(s-y))/(x0-xb)**2
obj = obj.subs({xa:-xa*xb, x0:-x0*xb}).subs({xb:xb/sqrt(q)})
# obj = (((x0*xb**2-q*s)*(1+2*x0*xb**2*(1+x0))+xb**2*(1+x0))*exp(-x0**2*xb**2)+(x0**2*xb**2+q*s)*exp(-xb**2))*exp(q*(s-y))/((x0+1)**2*xb**2)

# simple objective function is exp(q*(s-y))*(s*a+c)
simple_obj = simplify(s*abc[0] + abc[2])
# simple_obj = ((2*q*x0*(s+x0*xb)*(xb-x0)-s-x0**2+(xb-x0)**2)*exp(-q*x0**2)+(x0**2+s)*exp(-q*xb**2))/(x0-xb)**2
# simple_obj = ((2*q*x0**2*xb*(xb-x0)-x0**2+(xb-x0)**2)*exp(-q*x0**2)+x0**2*exp(-q*xb**2))/(x0-xb)**2
#				+s*((2*q*x0*(xb-x0)-1)*exp(-q*x0**2)+exp(-q*xb**2))/(x0-xb)**2
simple_obj = simple_obj.subs({xa:-xa*xb, x0:-x0*xb}).subs({xb:xb/sqrt(q)})
# simple_obj = (((x0*xb**2-q*s)*(1+2*x0*xb**2*(1+x0))+xb**2*(1+x0))*exp(-x0**2*xb**2)+(x0**2*xb**2+q*s)*exp(-xb**2))/((x0+1)**2*xb**2)

