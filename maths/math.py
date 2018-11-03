#
#   computation for mathematical expressions
#  ------------------------------------------
#
#  requires sympy to run, runs successfully with sympy version 1.1.1

from sympy import symbols, exp, simplify, diff, factor
from sympy.interactive.printing import init_printing
init_printing(use_unicode=False, wrap_line=False, no_global=True)
from sympy.matrices import Matrix

x0,xb,xa,s,y,q = symbols('x0, xb, xa, s, y, q')

# finding parabola (ax**2+bx+c) over exp(-x**2) for all xa<x<xb that minimises s*a+c
def f(x):
	return exp(-q*x**2)
m = Matrix([[xb*xb,xb,1],[x0*x0,x0,1],[2*x0,1,0]])
v = Matrix([[f(xb)],[f(x0)],[diff(f(x0),x0)]])
abc = factor(m.inv()*v)


# forx0 is height of the parabola above f(xa)
forx0 = simplify(abc[0]*xa**2 + abc[1]*xa + abc[2]-f(xa))
# testing that forx0 matches the expression:  (x0-xb)**2*((xa-xb)*(2*q*x0*(x0-xa)*(x0-xb)+2*x0-xa-xb)*exp(-q*x0**2)+(x0-xa)**2*exp(-q*xb**2)-(x0-xb)**2*exp(-q*xa**2))
test = simplify(forx0 - (  ((xa-xb)*(2*q*x0*(x0-xa)*(x0-xb)+2*x0-xa-xb)*exp(-q*x0**2)+(x0-xa)**2*exp(-q*xb**2)-(x0-xb)**2*exp(-q*xa**2))/(x0-xb)**2  ))
print "Testing correctness for forx0 expression: {}".format(test.is_zero)

# constructing objective function is exp(q*(s-y))*(s*a+c)
obj = simplify(exp(q*(s-y))*(s*abc[0] + abc[2]))
# testing that objective matches the expression:  (((s+x0*xb)*(2*q*x0*xb-2*q*x0**2-1)+xb*(xb-x0))*exp(-q*x0**2)+(s+x0**2)*exp(-q*xb**2))*exp(q*(s-y))/(x0-xb)**2
test = simplify(obj - (  (((s+x0*xb)*(2*q*x0*xb-2*q*x0**2-1)+xb*(xb-x0))*exp(-q*x0**2)+(s+x0**2)*exp(-q*xb**2))*exp(q*(s-y))/(x0-xb)**2  ))
print "Testing correctness for objective expression: {}".format(test.is_zero)

