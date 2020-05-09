from sympy import symbols, exp, simplify, diff, factor, expand, Sum, Rational
import sympy
from sympy.interactive.printing import init_printing
init_printing(use_unicode=False, wrap_line=False, no_global=True)
from sympy.matrices import Matrix
from sympy.solvers import solve
from sympy.abc import x,i,j
from sympy.core import Add, Mul
import pdb

a,b,D,t,s = symbols('a,b,D,t,s')

F = (b*exp(s*a) - a*exp(s*b))*exp(-s*t)/(b-a)

#F = F.subs({a:b-D})
diffF = diff(F,s)

diffF *= (b-a)*exp(s*t)
diffF = diffF.expand().simplify()

solF = F.subs({s:solve(diffF,s)[0]})

pdb.set_trace()
#print 



