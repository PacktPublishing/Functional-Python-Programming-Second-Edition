#!/usr/bin/env python3
"""Functional Python Programming

Chapter 3, Example Set 1
"""
from typing import Callable

class Mersenne1:
    """Callable object with a **Strategy** plug in required."""
    def __init__(self, algorithm: Callable[[int], int]) -> None:
        self.pow2 = algorithm
    def __call__(self, arg: int) -> int:
        return self.pow2(arg)-1

def shifty(b: int) -> int:
    """2**b via shifting.

    >>> shifty(17)-1
    131071
    """
    return 1 << b

def multy(b: int) -> int:
    """2**b via naive recursion.

    >>> multy(17)-1
    131071
    """
    if b == 0:
        return 1
    return 2*multy(b-1)

def faster(b: int) -> int:
    """2**b via faster divide-and-conquer recursion.

    >>> faster(17)-1
    131071
    """
    if b == 0:
        return 1
    if b%2 == 1:
        return 2*faster(b-1)
    t = faster(b//2)
    return t*t

# Implementations of Mersenne with strategy objects plugged in properly.

m1s = Mersenne1(shifty)
m1m = Mersenne1(multy)
m1f = Mersenne1(faster)

# Alternative Mersenne using class-level configuration.
# The syntax is awkward.

class Mersenne2:
    pow2: Callable[[int], int] = None
    def __call__(self, arg: int) -> int:
        pow2 = self.__class__.__dict__['pow2']
        return pow2(arg)-1

class ShiftyMersenne(Mersenne2):
    pow2 = shifty

class MultyMersenee(Mersenne2):
    pow2 = multy

class FasterMersenne(Mersenne2):
    pow2 = faster

m2s = ShiftyMersenne()
m2m = MultyMersenee()
m2f = FasterMersenne()

test_mersenne = """
>>> m1s(17)
131071
>>> m1m(17)
131071
>>> m1f(17)
131071
>>> m2s(17)
131071
>>> m2m(17)
131071
>>> m2f(17)
131071
>>> m1s(89)
618970019642690137449562111
>>> m1m(89)
618970019642690137449562111
>>> m1f(89)
618970019642690137449562111
"""

test_pure = """
>>> def m(n):
...     return 2**n-1
>>> m(89)
618970019642690137449562111
"""

__test__ = {
    'test_mersenne': test_mersenne,
    'test_pure': test_pure
}
def test():
    import doctest
    doctest.testmod(verbose=2)

def performance():
    import timeit
    print(m1s.pow2.__name__,
          timeit.timeit(
              """m1s(17)""",
              """from Chapter_3.ch03_ex1 import m1s"""))
    print(m1m.pow2.__name__,
          timeit.timeit(
              """m1m(17)""",
              """from Chapter_3.ch03_ex1 import m1m"""))
    print(m1f.pow2.__name__,
          timeit.timeit(
              """m1f(17)""",
              """from Chapter_3.ch03_ex1 import m1f"""))

if __name__ == "__main__":
    import sys
    print(sys.version)
    test()
    # import timeit
    # performance()
