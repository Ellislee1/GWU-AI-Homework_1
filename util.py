import numpy as np
from math import gcd
from functools import reduce


def is_valid_problem(pitchers: np.array, target: int) -> bool:
    """Returns true if there is a valid solution, false if there is not.

    The logic behind this stems from Bezout's identity, which relates an integer
    in terms of the gcd of other integers. More specifically, if d is the greatest
    common divisor of integers (a, b), then integers of the form ax + by are multiples
    of d. This idea can be generalized to more than 2 integers, which proves
    useful for this problem: a valid solution exists iff the target quantity is a 
    multiple of the gcd of all the pitcher values.
    
    More information: https://en.wikipedia.org/wiki/B%C3%A9zout%27s_identity#Generalizations
    """
    # get the gcd of all the pitchers
    x: int = reduce(gcd, pitchers)
    # problem is valid if the target is a multiple of the gcd
    return target % x == 0
