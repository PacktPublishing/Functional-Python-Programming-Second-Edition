#!/usr/bin/env python3
"""Functional Python Programming

Chapter 11, Example Set 2
"""
# pylint: disable=missing-docstring,wrong-import-position,reimported
from functools import wraps

def comp(func1):
    def abstract_decorator(func2):
        @wraps(func2)
        def composite(*args, **kw):
            return func1(func2(*args, **kw))
        return composite
    return abstract_decorator

def minus1(y):
    return y-1

@comp(minus1)
def pow2(x):
    return 2**x

example_1 = """
>>> pow2(17)
131071
"""

from typing import Callable
m1: Callable[[float], float] = lambda x: x-1
p2: Callable[[float], float] = lambda y: 2**y
mersenne: Callable[[float], float] = lambda x: m1(p2(x))

F_float = Callable[[float], float]

example_2 = """
>>> mersenne(17)
131071
"""

__test__ = {
    'example_1': example_1,
}

def test():
    import doctest
    doctest.testmod(verbose=1)

if __name__ == "__main__":
    test()
