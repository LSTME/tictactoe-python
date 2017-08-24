
from ttt import Game

import random
from itertools import product

import sys

class Mover:
    def __init__(self, n):
        self.c = set(product(range(n), repeat=2))

    def __call__(self, get, x, y, first):
        if not first:
            self.c.remove((x, y))
        r = random.choice(tuple(self.c))
        self.c.remove(r)
        return r

Game(sys.argv[1], sys.argv[2], Mover, "localhost", 32768).run()
