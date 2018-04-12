#!/usr/bin/env python3
"""Functional Python Programming

Chapter 10, Example Set 3
"""
# pylint: disable=wrong-import-position

from functools import partial

def performance():
    import timeit
    f1 = timeit.timeit("""exp2(12)""", setup="""
from functools import partial
exp2 = partial(pow, 2)""")
    print("partial", f1)

    f2 = timeit.timeit("""exp2(12)""", """exp2 = lambda y: pow(2, y)""")
    print("lambda", f2)

test_correctness = """
>>> exp2 = partial(pow, 2)
>>> exp2(12)
4096
>>> exp2(17)-1
131071
>>> exp2 = lambda y: pow(2, y)
>>> exp2(12)
4096
>>> exp2(17)-1
131071
"""

__test__ = {
    "test_correctness": test_correctness,
}

def test():
    import doctest
    doctest.testmod(verbose=1)

if __name__ == "__main__":
    test()
    performance()
