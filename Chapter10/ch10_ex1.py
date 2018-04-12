#!/usr/bin/env python3
"""Functional Python Programming

Chapter 10, Example Set 1
"""
# pylint: disable=wrong-import-position

def fib(n: int) -> int:
    """Fibonacci numbers with naive recursion

    >>> fib(20)
    6765
    >>> fib(1)
    1
    """
    if n == 0: return 0
    if n == 1: return 1
    return fib(n-1) + fib(n-2)

from functools import lru_cache

@lru_cache(maxsize=128)
def fibc(n: int) -> int:
    """Fibonacci numbers with naive recursion and caching

    >>> fibc(20)
    6765
    >>> fibc(1)
    1
    """
    if n == 0: return 0
    if n == 1: return 1
    return fibc(n-1) + fibc(n-2)

def performance_fib():
    import timeit

    f1 = timeit.timeit(
        """fib(20)""",
        setup="""from ch10_ex1 import fib""", number=1000)
    print("Naive", f1)

    f2 = timeit.timeit(
        """fibc(20); fibc.cache_clear()""",
        setup="""from ch10_ex1 import fibc""", number=1000)
    print("Cached", f2)

def nfact(n: int) -> int:
    """
    >>> nfact(5)
    120
    """
    if n == 0: return 1
    return n*nfact(n-1)

@lru_cache(maxsize=128)
def cfact(n: int) -> int:
    """
    >>> cfact(5)
    120
    """
    if n == 0: return 1
    return n*cfact(n-1)

from typing import Callable
def binom(p: int, r: int, fact: Callable[[int], int]) -> int:
    """
    >>> nfact(5)
    120
    >>> binom(52, 5, nfact)
    2598960
    >>> binom(52, 5, cfact)
    2598960
    """
    return fact(p)//(fact(r)*fact(p-r))

def performance_fact():
    import timeit

    f1 = timeit.timeit(
        """binom(52, 5, nfact)""",
        setup="""from ch10_ex1 import binom, nfact""", number=10000)
    print("Naive Factorial", f1)

    f2 = timeit.timeit(
        """binom(52, 5, cfact)""",
        setup="""from ch10_ex1 import binom, cfact""", number=10000)
    print("Cached Factorial, Dirty", f2)

    f3 = timeit.timeit(
        """binom(52, 5, cfact); cfact.cache_clear()""",
        setup="""from ch10_ex1 import binom, cfact""", number=10000)
    print("Cached Factorial, Cleared", f3)

def performance():
    performance_fib()
    performance_fact()

def test():
    import doctest
    doctest.testmod(verbose=1)

if __name__ == "__main__":
    test()
    performance()
