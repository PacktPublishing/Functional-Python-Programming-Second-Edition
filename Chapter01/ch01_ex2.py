#!/usr/bin/env python3
"""Functional Python Programming

Chapter 1, Example Set 2

Newton-Raphson root-finding via bisection.

http://www.cs.kent.ac.uk/people/staff/dat/miranda/whyfp90.pdf

Translated from Miranda to Python.
"""
from typing import Callable, Iterator

# next_ = lambda n, x: (x+n/x)/2

def next_(n: float, x: float) -> float:
    # pylint: disable=anomalous-backslash-in-string
    """
    ..  math::

        a_{i+1} = (a_i+n/a_i)/2

    Converges on

    ..  math::

        a = (a+n/a)/2

    So

    ..  math::

        2a  &= a+n/a \\
        a   &= n/a \\
        a^2 &= n \\
        a   &= \sqrt n
    """
    return (x+n/x)/2

def repeat(f: Callable[[float], float], a: float) -> Iterator[float]:
    """yields a, f(a), f(f(a)), etc."""
    yield a
    yield from repeat(f, f(a))

def within(eps: float, iterable: Iterator[float]) -> Iterator[float]:
    def head_tail(eps: float, a: float, iterable: Iterator[float]):
        b = next(iterable)
        if abs(a-b) <= eps:
            return b
        return head_tail(eps, b, iterable)

    return head_tail(eps, next(iterable), iterable)

def sqrt(a0: float, eps: float, n: float):
    return within(eps, repeat(lambda x: next_(n, x), a0))

def test():
    """
    >>> round(next_( 2, 1.5 ), 4)
    1.4167
    >>> n= 2
    >>> f= lambda x: next_( n, x )
    >>> a0= 1.0
    >>> [ round(x,4) for x in (a0, f(a0), f(f(a0)), f(f(f(a0))),) ]
    [1.0, 1.5, 1.4167, 1.4142]

    >>> within( .5, iter([3, 2, 1, .5, .25]) )
    0.5

    >>> round( sqrt( 1.0, .0001, 3 ), 6 )
    1.732051
    >>> round(1.732051**2, 5)
    3.0
    """
    import doctest
    doctest.testmod(verbose=1)

if __name__ == "__main__":
    test()
