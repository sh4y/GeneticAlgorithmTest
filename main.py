from Consumer import *
from Beer import *
import numpy as np
import matplotlib.pyplot as plt

INITIAL_BEER_POPULATION = 10
CONSUMER_POPULATION = 100
MATING_POOL_SIZE = 4 # N best beers per cycle
WORST_PERFORMER_DISCARD = 0.3
CROSSOVER_CHANCE = 0.5
MUTATE_CHANCE = 0.01
CONVERGENCE_REQUIREMENT = 100

def create_consumers(n):
    consumers = []
    # create n random consumers
    for x in range(n):
        con = Consumer()
        consumers.append(con)

    return consumers

def create_initial_beers(n):
    beers = []
    for x in range(n):
        beer = Beer()
        beers.append(beer)
    return beers

def evaluate_fitness(beers, consumers):
    beer_scores = []
    for beer in beers:
        beer_score = 0
        for consumer in consumers:
            score = consumer.evaluate_beer(beer)
            beer_score += score
        beer_scores.append(beer_score)
    return beer_scores

def build_mating_pool(best_beers_indices):
    mating_pool = []
    for i in range(MATING_POOL_SIZE):
        mating_pool.append(best_beers_indices[i])
    return mating_pool

def top_performer_mating(mating_pool, beers):
    # top performer mating
    children = []
    best_performer = beers[mating_pool[0]]
    for i in range(1, MATING_POOL_SIZE):
        index = mating_pool[i]
        child = best_performer.crossover(beers[index])
        children.append(child)
    return children

def sec_performer_mating(mating_pool ,beers):
    # second best performer
    children = []
    second_performer = beers[mating_pool[1]]
    for i in range(3):
        if random.random() <= 0.50:
            random_beer = random.choice(beers)
            child = second_performer.crossover(random_beer)
            children.append(child)
    return children

def worst_performer_mating(best_beers_indices, beers):
    children = []
    worst_performer = beers[best_beers_indices[len(best_beers_indices) - 1]]
    if random.random() <= 0.1:
        random_beer = random.choice(beers)
        child = worst_performer.crossover(random_beer)
        children.append(child)
    return children

def delete_bottom_beers(beers, best_beers_indices):
    length = len(beers)
    discard = math.ceil(WORST_PERFORMER_DISCARD * length)
    for i in range(discard):
        index = best_beers_indices[len(best_beers_indices) - 1 - i]
        del beers[index]

def create_children(beers, best_beers_indices):
    children = []
    mating_pool = build_mating_pool(best_beers_indices)
    children = children + top_performer_mating(mating_pool, beers)
    children = children + sec_performer_mating(mating_pool, beers)
    children = children + worst_performer_mating(best_beers_indices, beers)
    return children

def mutate_children(children):
    for child in children:
        child.mutate(MUTATE_CHANCE)

def average_fitness(beer_scores):
    return np.mean(beer_scores)

def converged(scores):
    last_n_scores = scores[-CONVERGENCE_REQUIREMENT:]
    stdev = np.std(last_n_scores)
    if (np.median(last_n_scores) + stdev < np.max(last_n_scores)):
        return False
    else:
        return True

def plot(array):
    plt.figure()
    plt.plot(array)
    plt.show()

# top performer will mate with the 3 other beers in mating pool
# second best performer has 75% chance (each) to mate with 3 other beers in mating pool
# worst performer has 30% chance to mate with random beer in beer pool

consumers = create_consumers(CONSUMER_POPULATION)
beers = create_initial_beers(INITIAL_BEER_POPULATION)
fitness_values = []
for i in range(5000):
    beer_scores = evaluate_fitness(beers, consumers)
    fitness_values.append(np.mean(beer_scores))
    best_beers_indices = sorted(np.argpartition(beer_scores, -len(beer_scores))[-len(beer_scores):], reverse=True)
    #print("Average fitness: " + str(average_fitness(beer_scores)))
    children = create_children(beers, best_beers_indices)
    mutate_children(children)
    delete_bottom_beers(beers, best_beers_indices)
    beers = beers + children
    for beer in beers:
        beer.adjust()
    if len(fitness_values) >= CONVERGENCE_REQUIREMENT:
        if converged(fitness_values):
            break

print("Beginning fitness: " + str(fitness_values[0]))
print("Median fitness:" + str(np.median(fitness_values)))
print("Max fitness: " + str(max(fitness_values)))
print("Current fitness: " + str(fitness_values[-1]))

#plt.axis([0,5000, 750,1000])
plt.plot(fitness_values)
plt.show()