import util
import random
import numpy as np
from deap import base
from deap import tools
from deap import creator
from deap import algorithms

def eval(locations, individual):
    
    distances = list(map(lambda x : util.haversine(individual, x), locations))
    
    return np.min(distances),


def run(location, radius, pop=100, n_hof=1, n_gen=100, test=False):

	if test:
		locations = util.get_test_data()
	else:
		locations = util.get_places(location, radius)
	
	(lat, lng) = location

	creator.create("FitnessMax", base.Fitness, weights=(1.0,))
	creator.create("Individual", list, fitness=creator.FitnessMax)

	toolbox = base.Toolbox()
	attr_loc = [lambda:util.get_lat_with_meter(lat, (random.random() * radius)), lambda:util.get_lng_with_meter(lat, lng, (random.random() * radius))]
	toolbox.register("individual", tools.initCycle, creator.Individual, attr_loc, 1)
	toolbox.register("population", tools.initRepeat, list, toolbox.individual)

	toolbox.register("evaluate", eval, locations)
	toolbox.register("mate", tools.cxTwoPoint)
	toolbox.register("mutate", tools.mutGaussian, mu=0, sigma=0.001, indpb=0.05)
	toolbox.register("select", tools.selTournament, tournsize=4)

	pop = toolbox.population(n=100)
	hof = tools.HallOfFame(3)
	stats = tools.Statistics(lambda ind: ind.fitness.values)

	stats.register("avg", np.mean)
	stats.register("std", np.std)
	stats.register("min", np.min)
	stats.register("max", np.max)

	pop, log = algorithms.eaSimple(pop, toolbox, cxpb=0.5, mutpb=0.2, ngen=100, stats=stats, halloffame=hof, verbose=False)

	lats = []
	longs = []

	for l in locations:
		lats.append(l[0])
		longs.append(l[1])
	
	return np.squeeze(hof.items), lats, longs