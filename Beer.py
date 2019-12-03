import random

class Beer:

    def __init__(self):
        self.initialize()

    def update_beer(self, efc, cost, taste):
        self.effectiveness = efc
        self.cost = cost
        self.taste = taste

    def initialize(self):
        self.effectiveness = random.uniform(0, 100)
        self.cost = random.uniform(0, 100)
        self.taste = random.uniform(0, 100)

    def crossover(self, otherBeer):
        chances = [random.random(), random.random(), random.random()]
        beer_traits = [self.effectiveness, self.cost, self.taste]
        other_beer_traits = [otherBeer.effectiveness, otherBeer.cost, otherBeer.taste]
        # if chance < 0.5, crossover takes other gene as base
        # if change >= 0.5, crossover keeps gene as base
        traits = []
        for x in range(len(chances)):
            min_trait = min(beer_traits[x], other_beer_traits[x]) #x1
            max_trait = max(beer_traits[x], other_beer_traits[x]) #x2

            boundary_start = min_trait - 0.5 * (max_trait-min_trait)
            boundary_end = max_trait + 0.5 * (max_trait-min_trait)

            traits.append(random.uniform(boundary_start, boundary_end))
            '''if chances[x] >= 0.5:
                base_value = beer_traits[x]
                modification =
                new_value = base_value + modification
                traits.append(new_value)
            else:
                base_value = other_beer_traits[x]
                modification = random.uniform(-(base_value // 20), (base_value // 20))
                new_value = base_value + modification
                traits.append(new_value)'''

        crossover_beer = Beer()
        crossover_beer.update_beer(traits[0], traits[1], traits[2])
        return crossover_beer

    def mutate(self, chance):
        if random.random() <= chance:
            values = [random.uniform(0, 40), random.uniform(0, 40), random.uniform(0, 40)]
            self.effectiveness += random.choice([-1,1]) * values[0]
            self.cost += random.choice([-1,1]) * values[1]
            self.taste += random.choice([-1,1]) * values[2]

    def adjust(self):
        if (self.effectiveness > 100):
            self.effectiveness = 100
        elif (self.effectiveness < 0):
            self.effectiveness = 0

        if (self.taste > 100):
            self.taste = 100
        elif  (self.taste < 0):
            self.taste = 0

        if (self.cost > 100):
            self.cost = 100
        elif (self.cost < 0):
            self.cost = 0
