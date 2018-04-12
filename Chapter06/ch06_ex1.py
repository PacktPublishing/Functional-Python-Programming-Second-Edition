#!/usr/bin/env python3
"""Functional Python Programming

Chapter 6, Example Set 1
"""
# pylint: disable=reimported,wrong-import-position

def add(a: int, b: int) -> int:
    """Recursive addition.

    >>> add( 3, 5 )
    8
    """
    if a == 0:
        return b
    elif b == 0:
        return a
    else: return add(a-1, b+1)

def fact(n: int) -> int:
    """Recursive Factorial

    >>> fact(0)
    1
    >>> fact(1)
    1
    >>> fact(7)
    5040
    """
    if n == 0:
        return 1
    else:
        return n*fact(n-1)

def facti(n: int) -> int:
    """Imperative Factorial

    >>> fact(0)
    1
    >>> fact(1)
    1
    >>> fact(7)
    5040
    """
    if n == 0:
        return 1
    f = 1
    for i in range(2, n):
        f = f*i
    return f

def fastexp(a: float, n: int) -> float:
    """Recursive exponentiation by squaring

    >>> fastexp( 3, 11 )
    177147
    """
    if n == 0:
        return 1
    elif n % 2 == 1:
        return a*fastexp(a, n-1)
    else:
        t = fastexp(a, n//2)
        return t*t

def fib(n: int) -> int:
    """Fibonacci numbers with naive recursion

    >>> fib(20)
    6765
    >>> fib(1)
    1
    """
    if n == 0:
        return 0
    if n == 1:
        return 1
    return fib(n-1) + fib(n-2)

def fibi(n: int) -> int:
    """Fibonacci numbers saving just two previous values

    >>> fibi(20)
    6765
    >>> fibi(1)
    1
    >>> fibi(2)
    1
    >>> fibi(3)
    2
    """
    if n == 0:
        return 0
    if n == 1:
        return 1
    f_n2, f_n1 = 1, 1
    for _ in range(3, n+1):
        f_n2, f_n1 = f_n1, f_n2+f_n1
    return f_n1

def fibi2(n: int) -> int:
    """Fibonacci numbers with iteration and memoization

    >>> fibi2(20)
    6765
    >>> fibi2(1)
    1
    """
    f = [0, 1] + [None for _ in range(2, n+1)]
    for i in range(2, n+1):
        f[i] = f[i-1]+f[i-2]
    return f[n]

from typing import Callable, Sequence, Any, List
def mapr(
        f: Callable[[Any], Any],
        collection: Sequence[Any]) -> List[Any]:
    """Recursive definition of map-like function.

    >>> mapr( lambda x:2**x, [0, 1, 2, 3, 4] )
    [1, 2, 4, 8, 16]
    """
    if len(collection) == 0:
        return []
    return mapr(f, collection[:-1]) + [f(collection[-1])]

from typing import Callable, Iterable, Iterator, Any, TypeVar
D_ = TypeVar("D_")
R_ = TypeVar("R_")
def mapf(f: Callable[[D_], R_], C: Iterable[D_]) -> Iterator[R_]:
    """Higher-Order definition of map.

    >>> list( mapf( lambda x:2**x, [0, 1, 2, 3, 4] ) )
    [1, 2, 4, 8, 16]
    """
    return (f(x) for x in C)

def mapg(f: Callable[[D_], R_], C: Iterable[D_]) -> Iterator[R_]:
    """Generator definition of map

    >>> list( mapg( lambda x:2**x, [0, 1, 2, 3, 4] ) )
    [1, 2, 4, 8, 16]
    """
    for x in C:
        yield f(x)

def prodi(items: Iterable[float]) -> float:
    """Imperative product

    >>> prodi( [1,2,3,4,5,6,7] )
    5040
    """
    p: float = 1
    for n in items:
        p *= n
    return p

def prodrc(collection: Sequence[float]) -> float:
    """Recursive product with a collection

    >>> prodrc( [1,2,3,4,5,6,7] )
    5040
    """
    if len(collection) == 0:
        return 1
    return collection[0] * prodrc(collection[1:])

def prodri(items: Iterator[float]) -> float:
    """Recursive product with an iterable

    >>> prodri( iter([1,2,3,4,5,6,7]) )
    5040
    """
    try:
        head = next(items)
    except StopIteration:
        return 1
    return head*prodri(items)


def test():
    import doctest
    doctest.testmod(verbose=1)

if __name__ == "__main__":
    test()
