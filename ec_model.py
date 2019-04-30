import util
import random
import numpy as np
from deap import base
from deap import tools
from deap import creator
from deap import algorithms

def eval(pharmacies, hospitals, individual):
    
	d_pharm = np.min(list(map(lambda x : util.haversine(individual, (x.latitude, x.longitude)), pharmacies)))
	
	if hospitals:	
		d_hosp = np.min(list(map(lambda x : util.haversine(individual, (x.latitude, x.longitude)), hospitals)))
	else:
		d_hosp = 0
    
	return d_pharm, d_hosp

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

def run(location, radius, population=100, n_gen=100, test=False, cxpb=0.5, mtpb=0.5):


	if test:
		(pharmacies, hospitals) = util.get_test_data()
	else:
		pharmacies = util.get_data(location, radius)
		hospitals = util.get_data(location, radius, query="hospitals")

	if not pharmacies:
		raise Exception("No pharmacies were found. You should consider increase the radius.")
	
	radius = radius
	(lat, lng) = location

	(min_lat, max_lat, min_long, max_long) = util.get_bounds(lat, lng, radius)

	creator.create("FitnessMulti", base.Fitness, weights=(1.0,-1.0))
	creator.create("Individual", list, fitness=creator.FitnessMulti)

	toolbox = base.Toolbox()
	attr_loc = [lambda:util.get_lat_with_meter(lat, radius), lambda:util.get_lng_with_meter(lat, lng, radius)]
	toolbox.register("individual", tools.initCycle, creator.Individual, attr_loc, 1)
	toolbox.register("population", tools.initRepeat, list, toolbox.individual)

	toolbox.register("evaluate", eval, pharmacies, hospitals)
	
	toolbox.register("mate", tools.cxSimulatedBinary, eta=20.0)
	toolbox.register("mutate", tools.mutGaussian, mu=0, sigma=0.0001, indpb=mtpb)

	toolbox.decorate("mate", checkBounds(min_lat, max_lat, min_long, max_long))
	toolbox.decorate("mutate", checkBounds(min_lat, max_lat, min_long, max_long))

	toolbox.register("select", tools.selNSGA2)

	stats = tools.Statistics(lambda ind: ind.fitness.values)

	
	stats.register("min", np.min, axis=0)
	stats.register("max", np.max, axis=0)
	stats.register("avg", np.mean, axis=0)
	stats.register("std", np.std, axis=0)

	logbook = tools.Logbook()
	logbook.header = "gen", "evals", "max", "min", "avg", "std"

	pop = toolbox.population(population)
	init_pop = pop.copy()
	pareto = tools.ParetoFront()

	invalid_ind = [ind for ind in pop if not ind.fitness.valid]
	fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
	for ind, fit in zip(invalid_ind, fitnesses):
		ind.fitness.values = fit

	# This is just to assign the crowding distance to the individuals
    # no actual selection is done
	pop = toolbox.select(pop, len(pop))
	pareto.update(pop)


	record = stats.compile(pop)
	logbook.record(gen=0, evals=len(invalid_ind), **record)

	for gen in range(1, n_gen):
		offspring = tools.selTournamentDCD(pop, len(pop))
		offspring = [toolbox.clone(ind) for ind in offspring]

		for ind1, ind2 in zip(offspring[::2], offspring[1::2]):
			if random.random() <= cxpb:
				toolbox.mate(ind1, ind2)

			toolbox.mutate(ind1)
			toolbox.mutate(ind2)
				
			del ind1.fitness.values, ind2.fitness.values
        
		# Evaluate the individuals with an invalid fitness
		invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
		fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
		for ind, fit in zip(invalid_ind, fitnesses):
			ind.fitness.values = fit

		# Select the next generation population
		pop = toolbox.select(pop + offspring, population)
		pareto.update(pop)

		record = stats.compile(pop)
		logbook.record(gen=gen, evals=len(invalid_ind), **record)

	if len(pareto.items) > 4:
		pareto_ind = pareto.items
		pareto = [pareto_ind[0], pareto_ind[round(2/4 * len(pareto_ind))], pareto_ind[round(3/4 * len(pareto_ind))], pareto_ind[-1]]
	
	return init_pop, logbook, pareto, pharmacies, hospitals