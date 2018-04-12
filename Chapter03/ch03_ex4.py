#!/usr/bin/env python3
"""Functional Python Programming

Chapter 3, Example Set 4
"""

import math
from typing import Iterator

def pfactorsl(x: int) -> Iterator[int]:
    """Loop/Recursion factors. Limited to numbers with 1,000 factors.

    >>> list(pfactorsl(1560))
    [2, 2, 2, 3, 5, 13]
    >>> list(pfactorsl(2))
    [2]
    >>> list(pfactorsl(3))
    [3]
    """
    if x % 2 == 0:
        yield 2
        if x//2 > 1:
            #for f in pfactorsl(x//2): yield f
            yield from pfactorsl(x//2)
        return
    for i in range(3, int(math.sqrt(x)+.5)+1, 2):
        if x % i == 0:
            yield i
            if x//i > 1:
                #for f in pfactorsl(x//i): yield f
                yield from pfactorsl(x//i)
            return
    yield x

def pfactorsr(x: int) -> Iterator[int]:
    """Pure Recursion factors. Limited to numbers below about 4,000,000

    >>> list(pfactorsr(1560))
    [2, 2, 2, 3, 5, 13]
    >>> list(pfactorsr(2))
    [2]
    >>> list(pfactorsr(3))
    [3]
    """
    def factor_n(x: int, n: int) -> Iterator[int]:
        if n*n > x:
            yield x
            return
        if x % n == 0:
            yield n
            if x//n > 1:
                #for f in factor_n( x // n, n ): yield f
                yield from factor_n(x // n, n)
        else:
            #for f in factor_n( x, n+2 ): yield f
            yield from factor_n(x, n+2)
    if x % 2 == 0:
        yield 2
        if x//2 > 1:
            #for f in pfactorsr( x//2 ): yield f
            yield from pfactorsr(x//2)
        return
    #for f in factor_n( x, 3 ): yield f
    yield from factor_n(x, 3)

def divisorsr(n: int, a: int=1) -> Iterator[int]:
    """Recursive divisors of n

    >>> list(divisorsr( 26 ))
    [1, 2, 13]
    """
    if a == n:
        return
    if n % a == 0:
        yield a
    #for d in divisorsr( n, a+1 ): yield d
    yield from divisorsr(n, a+1)

def divisorsi(n):
    """Imperative divisors of n

    >>> list(divisorsi( 26 ))
    [1, 2, 13]
    """
    return (a for a in range(1, n) if n%a == 0)

def perfect(n):
    """Perfect numbers test

    >>> perfect( 6 )
    True
    >>> perfect( 28 )
    True
    >>> perfect( 26 )
    False
    >>> perfect( 496 )
    True
    """
    return sum(divisorsr(n, 1)) == n

import itertools
from typing import Iterable, Any
def limits(iterable: Iterable[Any]) -> Any:
    """
    >>> limits([1, 2, 3, 4, 5])
    (5, 1)
    """
    max_tee, min_tee = itertools.tee(iterable, 2)
    return max(max_tee), min(min_tee)

def test():
    import doctest
    doctest.testmod(verbose=1)

if __name__ == "__main__":
    test()
