#!/usr/bin/env python3
"""Functional Python Programming

Chapter 13, Example Set 1
"""
# pylint: disable=unused-wildcard-import,wrong-import-position,unused-import

from typing import Iterable
from functools import reduce
def prod(data: Iterable[int]) -> int:
    """
    >>> prod((1,2,3))
    6
    """
    return reduce(lambda x, y: x*y, data, 1)

year_cheese = [
    (2000, 29.87), (2001, 30.12), (2002, 30.6), (2003, 30.66),
    (2004, 31.33), (2005, 32.62), (2006, 32.73), (2007, 33.5),
    (2008, 32.84), (2009, 33.02), (2010, 32.92)
]

from typing import Callable, Sequence, TypeVar
T_ = TypeVar("T_")
fst: Callable[[Sequence[T_]], T_] = lambda x: x[0]
snd: Callable[[Sequence[T_]], T_] = lambda x: x[1]

x = min(year_cheese, key=snd)


test_itemgetter = """
>>> from operator import itemgetter
>>> itemgetter(0)([1, 2, 3])
1
>>> min(year_cheese, key=snd)
(2000, 29.87)
>>> max(year_cheese, key=itemgetter(1))
(2007, 33.5)
"""

# from collections import namedtuple
# YearCheese = namedtuple( "YearCheese", ("year", "cheese") )'

from typing import NamedTuple
class YearCheese(NamedTuple):
    year: int
    cheese: float

year_cheese_2 = list(YearCheese(*yc) for yc in year_cheese)

test_year_cheese_2 = """
>>> year_cheese_2  # doctest: +NORMALIZE_WHITESPACE
[YearCheese(year=2000, cheese=29.87), YearCheese(year=2001, cheese=30.12),
 YearCheese(year=2002, cheese=30.6), YearCheese(year=2003, cheese=30.66),
 YearCheese(year=2004, cheese=31.33), YearCheese(year=2005, cheese=32.62),
 YearCheese(year=2006, cheese=32.73), YearCheese(year=2007, cheese=33.5),
 YearCheese(year=2008, cheese=32.84), YearCheese(year=2009, cheese=33.02),
 YearCheese(year=2010, cheese=32.92)]
"""

test_attrgetter = """
>>> from operator import attrgetter
>>> min( year_cheese_2, key=attrgetter('cheese') )
YearCheese(year=2000, cheese=29.87)
>>> max( year_cheese_2, key=lambda x: x.cheese )
YearCheese(year=2007, cheese=33.5)
"""

g_f = [
    1, 1/12, 1/288, -139/51840, -571/2488320, 163879/209018880,
    5246819/75246796800
]

g = [
    (1, 1), (1, 12), (1, 288), (-139, 51840),
    (-571, 2488320), (163879, 209018880),
    (5246819, 75246796800)
]

from itertools import starmap

from fractions import Fraction
test_starmap1 = """
>>> from operator import truediv
>>> round( sum( starmap( truediv, g ) ), 6 )
1.084749
>>> round( sum( g_f ), 6 )
1.084749
>>> f= sum( Fraction(*x) for x in g )
>>> f
Fraction(81623851739, 75246796800)
>>> round( float(f), 6 )
1.084749
"""

from itertools import zip_longest

test_starmap2 = """
>>> from operator import truediv
>>> p = (3, 8, 29, 44)
>>> d = starmap( pow, zip_longest([], range(4), fillvalue=60) )
>>> pi = sum( starmap( truediv, zip( p, d ) ) )
>>> pi
3.1415925925925925
>>> d = starmap( pow, zip_longest([], range(4), fillvalue=60) )
>>> pi = sum( map( truediv, p, d ) )
>>> pi
3.1415925925925925
"""

def fact(n: int) -> int:
    """
    >>> fact(0)
    1
    >>> fact(1)
    1
    >>> fact(2)
    2
    >>> fact(3)
    6
    >>> fact(4)
    24
    """
    f = {
        n == 0: lambda n: 1,
        n == 1: lambda n: 1,
        n == 2: lambda n: 2,
        n > 2: lambda n: fact(n-1)*n
    }[True]
    return f(n)

from typing import Callable, Tuple, List

from operator import itemgetter
def semifact(n: int) -> int:
    """
    >>> semifact(0)
    1
    >>> semifact(1)
    1
    >>> semifact(2)
    2
    >>> semifact(3)
    3
    >>> semifact(4)
    8
    >>> semifact(5)
    15
    >>> semifact(9)
    945
    """
    alternatives: List[Tuple[bool, Callable[[int], int]]] = [
        (n == 0, lambda n: 1),
        (n == 1, lambda n: 1),
        (n == 2, lambda n: 2),
        (n > 2, lambda n: semifact(n-2)*n)
    ]
    _, f = next(filter(itemgetter(0), alternatives))
    return f(n)

def semifact2(n: int) -> int:
    """
    >>> semifact2(9)
    945
    """
    alternatives = [
        (lambda n: 1) if n == 0 else None,
        (lambda n: 1) if n == 1 else None,
        (lambda n: 2) if n == 2 else None,
        (lambda n: semifact2(n-2)*n) if n > 2 else None
    ]
    f = next(filter(None, alternatives))
    return f(n)

# Here's a "stub" definition for a class that includes
# the minimal feature set for comparison.
# These are often in a module in the `stubs` directory.

from abc import ABCMeta, abstractmethod
from typing import TypeVar, Any

# pylint: disable=pointless-statement,multiple-statements
class Rankable(metaclass=ABCMeta):
    @abstractmethod
    def __lt__(self, other: Any) -> bool: ...
    @abstractmethod
    def __gt__(self, other: Any) -> bool: ...
    @abstractmethod
    def __le__(self, other: Any) -> bool: ...
    @abstractmethod
    def __ge__(self, other: Any) -> bool: ...

RT = TypeVar('RT', bound=Rankable)

def non_strict_max(a: RT, b: RT) -> RT:
    """
    >>> non_strict_max( 2, 2 )
    2
    >>> non_strict_max( 3, 5 )
    5
    >>> non_strict_max( 11, 7 )
    11
    """
    f = {a >= b: lambda: a, b >= a: lambda: b}[True]
    return f()

test_starmap3 = """
>>> from itertools import count, takewhile
>>> from operator import truediv
>>> num = map(fact, count())
>>> den = map(semifact, (2*n+1 for n in count()))
>>> terms = takewhile(
...     lambda t: t > 1E-15, map(truediv, num, den))
>>> round( float(2*sum(terms)), 8 )
3.14159265
"""

test_reduction = """
>>> import functools, operator
>>> sum=  functools.partial( functools.reduce, operator.add )
>>> sum([1,2,3])
6
>>> prod = functools.partial( functools.reduce, operator.mul )
>>> prod( [1,2,3,4] )
24
>>> fact = lambda n: 1 if n < 2 else n*prod( range(1,n) )
>>> fact(4)
24
>>> fact(0)
1
>>> fact(1)
1
"""

test_unordered = """
>>> {'a': 1, 'a': 2}
{'a': 2}
"""

__test__ = {
    "test_itemgetter": test_itemgetter,
    "test_attrgetter": test_attrgetter,
    "test_year_cheese_2": test_year_cheese_2,
    "test_starmap1": test_starmap1,
    "test_starmap2": test_starmap2,
    "test_starmap3": test_starmap3,
    "test_reduction": test_reduction,
    "test_unordered": test_unordered,
}

def test():
    import doctest
    doctest.testmod(verbose=1)

if __name__ == "__main__":
    test()
