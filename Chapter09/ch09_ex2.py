#!/usr/bin/env python3
"""Functional Python Programming

Chapter 9, Example Set 2

An example of an optimization problem:

https://www.me.utexas.edu/~jensen/ORMM/models/unit/combinatorics/permute.html

"""
# pylint: disable=wildcard-import,unused-wildcard-import,wrong-import-position

import csv
import io

# Cost data
cost_data = """\
14,11,6,20,12,9,4
15,28,34,4,12,24,21
16,31,22,18,31,15,23
20,18,9,15,30,4,18
24,8,24,30,28,25,4
3,23,22,11,5,30,5
13,7,5,10,7,7,32
"""

from typing import List, Tuple
def get_cost_matrix() -> List[Tuple[int, ...]]:
    with io.StringIO(cost_data) as source:
        rdr = csv.reader(source)
        cost = list(tuple(map(int, row)) for row in rdr)
    return cost

from itertools import *

def assignment(cost: List[Tuple[int, ...]]) -> List[Tuple[int, ...]]:
    n = len(cost)
    perms = permutations(range(n))
    alt = [
        (
            sum(
                cost[x][y] for y, x in enumerate(perm)
            ),
            perm
        )
        for perm in perms
    ]
    m = min(alt)[0]
    return [ans for s, ans in alt if s == m]

test_assignment = """
>>> from pprint import pprint
>>> cost= get_cost_matrix()
>>> len(cost)
7
>>> pprint(cost)
[(14, 11, 6, 20, 12, 9, 4),
 (15, 28, 34, 4, 12, 24, 21),
 (16, 31, 22, 18, 31, 15, 23),
 (20, 18, 9, 15, 30, 4, 18),
 (24, 8, 24, 30, 28, 25, 4),
 (3, 23, 22, 11, 5, 30, 5),
 (13, 7, 5, 10, 7, 7, 32)]

>>> solutions = assignment(cost)
>>> pprint(solutions)
[(2, 4, 6, 1, 5, 3, 0), (2, 6, 0, 1, 5, 3, 4)]

>>> expected= tuple(map(lambda x:x-1, [3,5,7,2,6,4,1] ) )
>>> expected
(2, 4, 6, 1, 5, 3, 0)
>>> expected in solutions
True
"""

def performance():
    """Takes almost 1 minute."""
    import timeit
    perf = timeit.timeit(
        """list(permutations(range(10)))""",
        """from itertools import permutations""",
        number=100)

    print("10!", perf/100)

test_combinations = """
>>> hands= list(combinations( tuple(product(range(13),'♠♥♦♣')), 5 ))
>>> print( len(hands) )
2598960
"""

__test__ = {
    "test_assignment": test_assignment,
    "test_combinations": test_combinations,
}

def test():
    import doctest
    doctest.testmod(verbose=1)

if __name__ == "__main__":
    #performance()

    test()
