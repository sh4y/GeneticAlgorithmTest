import random, math
class Consumer:
    def __init__(self):
        # the higher it is, the more the consumer likes higher costing alcohol
        self.affluence = random.uniform(0, 100)
        # the closer the taste matches the taste variable in the beer, the better it is
        self.taste = random.uniform(0, 100)
        # the higher it is, the more weight the consumer places on the effectiveness of the alcohol
        self.drunkenness = random.uniform(0, 100)

    def evaluate_beer(self, beer):
        # value of money
        # range = 0, 100
        vom = pow((self.affluence + beer.cost) / 100, 2)
        # value of taste
        # same reasoning as vom, closer the values, the better it is.
        vot = math.sqrt(10000 - math.pow((abs(self.taste - beer.taste)),2))
        # value of effectiveness
        voe = 100 * (self.drunkenness + beer.effectiveness / (beer.effectiveness+0.01))

        final_score = math.sqrt(vom)
        return final_score   