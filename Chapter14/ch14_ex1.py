#!/usr/bin/env python3
"""Functional Python Programming

Chapter 14, Example Set 1
"""
from pymonad import curry, Just, Nothing, List

@curry
def systolic_bp(bmi, age, gender_male, treatment):
    """
    Example of multiple regression model.

    See http://sphweb.bumc.bu.edu/otlt/MPH-Modules/BS/BS704_Multivariable/BS704_Multivariable7.html
    """
    return (
        68.15+0.58*bmi+0.65*age+0.94*gender_male+6.44*treatment
    )

tests_curry_1 = """
>>> systolic_bp( 25, 50, 1, 0 )
116.09
>>> systolic_bp( 25, 50, 0, 1 )
121.59
>>> treated = systolic_bp( 25, 50, 0 )
>>> treated(0)
115.15
>>> treated(1)
121.59
>>> g_t= systolic_bp( 25, 50 )
>>> g_t(1, 0)
116.09
>>> g_t(0, 1)
121.59
"""

from collections.abc import Sequence

@curry
def myreduce(function, iterable_or_sequence):
    if isinstance(iterable_or_sequence, Sequence):
        iterator = iter(iterable_or_sequence)
    else:
        iterator = iterable_or_sequence
    s = next(iterator)
    for v in iterator:
        s = function(s, v)
    return s

test_curry_2 = """
>>> from operator import *
>>> sum= myreduce( add )
>>> sum( [1,2,3] )
6
>>> max= myreduce( lambda x,y: x if x > y else y )
>>> max( [2,5,3] )
5
"""

def f(x, *args):
    def f1(y, *args):
        def f2(z):
            return (x+y)*z
        if args:
            return f2(*args)
        return f2
    if args:
        return f1(*args)
    return f1

test_manual_curry = """
>>> f(2)(3)(5)
25
>>> f(3,5,7)
56
>>> f(5,7)(9)
108
"""

import operator

prod = myreduce(operator.mul)

@curry
def alt_range(n):
    if n == 0:
        return range(1, 2)  # Only 1
    elif n % 2 == 0:
        return range(2, n+1, 2)
    else:
        return range(1, n+1, 2)

@curry
def range1n(n):
    if n == 0:
        return range(1, 2)  # Only 1
    return range(1, n+1)

test_composition = """
>>> semi_fact= prod * alt_range
>>> semi_fact(9)
945
>>> semi_fact(1)
1
>>> semi_fact(2)
2
>>> semi_fact(3)
3
>>> semi_fact(4)
8
>>> semi_fact(5)
15
>>> fact= prod * range1n
>>> fact(1)
1
>>> fact(2)
2
>>> fact(3)
6
>>> semi_fact(0)
1
>>> fact(1)
1
"""

test_functor = """
>>> x1= systolic_bp * Just(25) & Just(50) & Just(1) & Just(0)
>>> x1.getValue()
116.09
>>> x2= systolic_bp * Just(25) & Just(50) & Just(1) & Nothing
>>> x2.getValue() is None
True

>>> pi = lambda: 3.14
>>> pi()
3.14
"""

@curry
def n21(n):
    """
    >>> n21(0)
    1
    >>> n21(1)
    2
    """
    return 2*n+1

test_functor2 = """
>>> fact= prod * range1n
>>> seq1 = List(*range(20))
>>> f1=fact * seq1
>>> f1[:10]
[1, 1, 2, 6, 24, 120, 720, 5040, 40320, 362880]

>>> semi_fact= prod * alt_range
>>> f2=semi_fact * n21 * seq1
>>> f2[:10]
[1, 3, 15, 105, 945, 10395, 135135, 2027025, 34459425, 654729075]

>>> 2*sum(map( operator.truediv, f1, f2 ))
3.1415919276751456
"""

test_bind = """
>>> fact= prod * range1n
>>> r= Just(3) >> Just * fact
>>> r.getValue()
6
"""

__test__ = {
    "tests_curry_1": tests_curry_1,
    "test_curry_2": test_curry_2,
    "test_manual_curry": test_manual_curry,
    "test_composition": test_composition,
    "test_functor": test_functor,
    "test_functor2": test_functor2,
    "test_bind": test_bind,
}

def test():
    import doctest
    doctest.testmod(verbose=1)

if __name__ == "__main__":
    test()
