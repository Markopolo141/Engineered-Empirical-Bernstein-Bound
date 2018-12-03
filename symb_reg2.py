import pdb
import numpy as np
import operator
import math
import random
from math import exp

from deap import algorithms
from deap import base
from deap import creator
from deap import tools
from deap import gp


def fit_supervenient_function(func, args, len_points, operators, population_size=2000, generations=2000, crossover_prob=0.2, mutation_prob=0.04, height_limit=17, seed=318, gen_min=3, gen_max=6, tournsize=3, mut_min=0, mut_max=3):
	points = 0
	data = []
	while (points < len_points):
		d = [random.random()*(a[2]-a[1])+a[1] for a in args]
		f = func(*d)
		if f is not None:
			data.append([f,d[:]])
			points += 1
	pset = gp.PrimitiveSet("MAIN", len(args))
	for o in operators:
		pset.addPrimitive(o[0], o[1])
	#pset.addEphemeralConstant("rand101", lambda: random.randint(-1,1))
	pset.addEphemeralConstant("rand101", lambda: random.random()*2-1)
	pset.renameArguments(**{"ARG{}".format(i):a[0] for i,a in enumerate(args)})
	def evalSymbReg(individual, data):
		func = toolbox.compile(expr=individual)
		err = 0
		for i in range(len(data)):
			try:
				e = func(*data[i][1])-data[i][0]
			#if e>=0:
				err += abs(e)#e**2
			except:
				return 10000.0,
			#else:
			#	err=99999999
			#	break
		err += 0.0001*individual.height
		return err,
	creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
	creator.create("Individual", gp.PrimitiveTree, fitness=creator.FitnessMin)
	toolbox = base.Toolbox()
	toolbox.register("expr", gp.genHalfAndHalf, pset=pset, min_=gen_min, max_=gen_max)
	toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.expr)
	toolbox.register("population", tools.initRepeat, list, toolbox.individual)
	toolbox.register("compile", gp.compile, pset=pset)
	toolbox.register("evaluate", evalSymbReg, data=data)
	toolbox.register("select", tools.selTournament, tournsize=tournsize)
	toolbox.register("mate", gp.cxOnePoint)
	toolbox.register("expr_mut", gp.genFull, min_=mut_min, max_=mut_max)
	toolbox.register("mutate", gp.mutUniform, expr=toolbox.expr_mut, pset=pset)
	toolbox.decorate("mate", gp.staticLimit(key=operator.attrgetter("height"), max_value=height_limit))
	toolbox.decorate("mutate", gp.staticLimit(key=operator.attrgetter("height"), max_value=height_limit))
	
	random.seed(seed)
	pop = toolbox.population(n=population_size)
	hof = tools.HallOfFame(1)
	stats_fit = tools.Statistics(lambda ind: ind.fitness.values)
	stats_size = tools.Statistics(len)
	mstats = tools.MultiStatistics(fitness=stats_fit, size=stats_size)
	mstats.register("avg", np.mean)
	mstats.register("std", np.std)
	mstats.register("min", np.min)
	mstats.register("max", np.max)

	pop, log = algorithms.eaSimple(pop, toolbox, crossover_prob, mutation_prob, generations, stats=mstats, halloffame=hof, verbose=True)
	#print log
	return pop, log, hof



def forx0(xb,xa,x0): # returns hight of parabola above exp(-xa**2*xb**2) for parabola passing though exp(-xb**2) and tangentially through exp(-x0**2*xb**2) for 0<=x0<=xa<=1
	if x0>xa:
		return float('nan')
	return (xa+1)*(2*x0*xb**2*(x0+1)*(x0-xa)+2*x0-xa+1)*exp(-x0**2*xb**2)-(x0+1)**2*exp(-xa**2*xb**2)+(x0-xa)**2*exp(-xb**2)
def find_zero(xb,xa): # finds x0 that solves forx0=0 for given xb,xa
	x0 = 0.0
	for i in range(1,25):
		pi = 1.0/np.power(2,i)
		if (x0+pi<=xa) and (forx0(xb,xa,x0+pi)>0):
			x0 += pi
	return x0


def func(x):
	return find_zero(x,0.4)
args = [['x',0.01,10.0]]

def safeexp(x):
	if x>100.0:
		return exp(100.0)
	return exp(x)

operators = [
	[operator.add, 2],
	[operator.sub, 2],
	[operator.mul, 2],
	[operator.neg, 1],
	[safeexp,1]
]

from sympy import symbols, simplify
import sympy

if __name__ == "__main__":
	top = str(fit_supervenient_function(func, args, 350, operators)[2][0])
	context = {}
	for a in args:
		context[a[0]]=symbols(a[0])
	context['add']=lambda x,y : x+y
	context['sub']=lambda x,y : x-y
	context['mul']=lambda x,y : x*y
	context['neg']=lambda x:-x
	context['safeexp']=lambda x:sympy.exp(x)
	print simplify(eval(top,context))



