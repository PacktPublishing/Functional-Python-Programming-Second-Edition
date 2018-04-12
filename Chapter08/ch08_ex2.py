#!/usr/bin/env python3
"""Functional Python Programming

Chapter 8, Example Set 2
"""
# pylint: disable=wrong-import-position
from itertools import count
from typing import Callable, Iterator, TypeVar, Tuple

Generator = Iterator[Tuple[float, float]]
source: Generator = zip(count(0, 0.1), (.1*c for c in count()))

Extractor = Callable[[Tuple[float, float]], float]
x: Extractor = lambda x_y: x_y[0]
y: Extractor = lambda x_y: x_y[1]

Comparator = Callable[[Tuple[float, float]], bool]
neq: Comparator = lambda xy: abs(x(xy)-y(xy)) > 1.0E-12

T_ = TypeVar("T_")
def until(
        terminate: Callable[[T_], bool],
        iterator: Iterator[T_]
    ) -> T_:
    i = next(iterator)
    if terminate(i):
        return i
    return until(terminate, iterator)

accumulated_error_1 = """
>>> until(neq, source)
(92.799999999999, 92.80000000000001)
"""

def until_i(
        terminate: Callable[[T_], bool],
        iterator: Iterator[T_]) -> T_:
    for i in iterator:
        if terminate(i):
            return i
    raise StopIteration

accumulated_error_2 = """
>>> source_2 = zip(count(0, .1), (.1*c for c in count()))
>>> x = lambda x_y: x_y[0]
>>> y = lambda x_y: x_y[1]
>>> neq6: Callable[[Tuple[float, float]], bool] = lambda xy: abs(x(xy)-y(xy)) > 1.0E-6
>>> until_i(neq6, source_2)
(94281.30000100001, 94281.3)
>>> source_3 = zip( count(0, 1/35), (c/35 for c in count()) )
>>> until_i(neq6, source_3)
(73143.51428471429, 73143.5142857143)
>>> source_4 = zip( count(0, 1/35), (c/35 for c in count()) )
>>> until_i(lambda xy: x(xy) != y(xy), source_4)
(0.2285714285714286, 0.22857142857142856)
"""

fizz_buzz = """
# Silly fizz-buzz-like problem.
>>> from itertools import cycle
>>> m3 = (i == 0 for i in cycle(range(3)))
>>> m5 = (i == 0 for i in cycle(range(5)))
>>> multipliers = zip(range(10), m3, m5)
>>> list(multipliers)
[(0, True, True), (1, False, False), (2, False, False), (3, True, False), (4, False, False), (5, False, True), (6, True, False), (7, False, False), (8, False, False), (9, True, False)]

>>> m3 = (i == 0 for i in cycle(range(3)))
>>> m5 = (i == 0 for i in cycle(range(5)))
>>> multipliers = zip(range(10), m3, m5)
>>> total = sum(i
...    for i, *multipliers in multipliers
...    if any(multipliers))
>>> total
23
"""

file_filter = """
>>> import io
>>> import csv
>>> from itertools import cycle, compress
>>> chooser = (x == 0 for x in cycle(range(3)))
>>> with open("Anscombe.txt") as source_file:
...    rdr= csv.reader( source_file, delimiter="\\t" )
...    #keep= (row for pick, row in zip(chooser, rdr) if pick)
...    keep= tuple( compress( rdr, chooser ) )
>>> for row in keep:
...    print( row )
["Anscombe's quartet"]
['10.0', '8.04', '10.0', '9.14', '10.0', '7.46', '8.0', '6.58']
['9.0', '8.81', '9.0', '8.77', '9.0', '7.11', '8.0', '8.84']
['6.0', '7.24', '6.0', '6.13', '6.0', '6.08', '8.0', '5.25']
['7.0', '4.82', '7.0', '7.26', '7.0', '6.42', '8.0', '7.91']
"""

repeater = """
>>> import random
>>> from itertools import cycle, repeat, compress
>>> all = repeat(0)
>>> subset = cycle(range(3))
>>> def randseq(limit):
...     while True:
...         yield random.randrange(limit)
>>> randomized = randseq(3)
>>> choose = lambda rule: (x == 0 for x in rule)
>>> random.seed(1)
>>> data = [random.randint(1,12) for _ in range(12)]
>>> data
[3, 10, 2, 5, 2, 8, 8, 8, 11, 7, 4, 2]
>>> [v for v, pick in zip(data, choose(all)) if pick]
[3, 10, 2, 5, 2, 8, 8, 8, 11, 7, 4, 2]
>>> [v for v, pick in zip(data, choose(subset)) if pick]
[3, 5, 8, 7]
>>> random.seed(1)
>>> [v for v, pick in zip(data, choose(randomized)) if pick]
[3, 2, 2, 4, 2]

>>> list(compress(data, choose(all)))
[3, 10, 2, 5, 2, 8, 8, 8, 11, 7, 4, 2]
>>> list(compress(data, choose(subset)))
[3, 5, 8, 7]
>>> random.seed(1)
>>> list(compress(data, choose(randomized)))
[3, 2, 2, 4, 2]

"""

squares = """
>>> from itertools import repeat
>>> squares = list(sum(repeat(i, times=i)) for i in range(10))
>>> print( squares )
[0, 1, 4, 9, 16, 25, 36, 49, 64, 81]

"""

__test__ = {
    "accumulated_error_1": accumulated_error_1,
    "accumulated_error_2": accumulated_error_2,
    "fizz_buzz": fizz_buzz,
    "file_filter": file_filter,
    "repeat": repeater,
    "squares": squares,
}

def test():
    import doctest
    doctest.testmod(verbose=True)

if __name__ == "__main__":
    test()
