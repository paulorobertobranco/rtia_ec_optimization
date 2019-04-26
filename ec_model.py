import util
import random
import numpy as np
from deap import base
from deap import tools
from deap import creator
from deap import algorithms

def eval(data, individual):
    
	distances = list(map(lambda x : util.haversine(individual, (x.latitude, x.longitude)), data))
    
	return np.min(distances),

def checkBounds(min_lat, max_lat, min_long, max_long):
    def decorator(func):
        def wrapper(*args, **kargs):
            offspring = func(*args, **kargs)
            for child in offspring:
                if child[0] > max_lat:
                    child[0] = max_lat
                elif child[0] < min_lat:
                    child[0] = min_lat
                if child[1] > max_long:
                    child[1] = max_long
                elif child[1] < min_long:
                    child[1] = min_long
            return offspring
        return wrapper
    return decorator

def run(location, radius, pop=100, n_hof=1, n_gen=100, test=False):


	if test:
		data = util.get_test_data()
	else:
		data = util.get_data(location, radius)

	if not data:
		raise Exception("No pharmacies were found. You should consider increase the radius.")
	
	radius = radius * 2
	(lat, lng) = location

	(min_lat, max_lat, min_long, max_long) = util.get_bounds(lat, lng, radius)

	creator.create("FitnessMax", base.Fitness, weights=(1.0,))
	creator.create("Individual", list, fitness=creator.FitnessMax)

	toolbox = base.Toolbox()
	attr_loc = [lambda:util.get_lat_with_meter(lat, radius), lambda:util.get_lng_with_meter(lat, lng, radius)]
	toolbox.register("individual", tools.initCycle, creator.Individual, attr_loc, 1)
	toolbox.register("population", tools.initRepeat, list, toolbox.individual)

	toolbox.register("evaluate", eval, data)
	toolbox.register("mate", tools.cxOnePoint)
	toolbox.register("mutate", tools.mutGaussian, mu=0, sigma=0.0001, indpb=0.05)

	toolbox.decorate("mate", checkBounds(min_lat, max_lat, min_long, max_long))
	toolbox.decorate("mutate", checkBounds(min_lat, max_lat, min_long, max_long))

	toolbox.register("select", tools.selTournament, tournsize=3)

	pop = toolbox.population(pop)
	init_pop = pop.copy()
	hof = tools.HallOfFame(n_hof)
	stats = tools.Statistics(lambda ind: ind.fitness.values)

	stats.register("avg", np.mean)
	stats.register("std", np.std)
	stats.register("min", np.min)
	stats.register("max", np.max)

	pop, log = algorithms.eaSimple(pop, toolbox, cxpb=0.5, mutpb=0.2, ngen=n_gen, stats=stats, halloffame=hof, verbose=False)

	return init_pop, log, hof, data