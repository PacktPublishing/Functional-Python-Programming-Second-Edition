#!/usr/bin/env python3
"""Functional Python Programming

Chapter 8, Example Set 3
"""
# pylint: disable=reimported,wrong-import-position,wrong-import-order

from itertools import (
    accumulate, repeat, chain, starmap, tee, dropwhile, islice, groupby
    )

# Accumulate
# repeat(8128, times=13) -- only the first value is used
# other 13 are to create a sequence of values to drive the generator function

from typing import List
def digits_fixed(value: int, digits: int, base: int) -> List[int]:
    """
    >>> digits_fixed(8128, 16, 2)
    [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0]
    """
    digits_reversed = (
        x % base
        for x in accumulate(
            repeat(value, digits), func=lambda x, y: x//base
        )
    )
    return list(reversed(list(digits_reversed)))

from typing import Callable, Iterator, TypeVar
T_ = TypeVar("T_")
def while_not(
        terminate: Callable[[T_], bool],
        iterator: Iterator[T_]
    ) -> Iterator[T_]:
    """Iterator which terminates."""
    i = next(iterator)
    if terminate(i):
        return
    yield i
    yield from while_not(terminate, iterator)

def digits_variable(value: int, base: int) -> List[int]:
    """
    >>> digits_variable(8128, 2)
    [1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0]
    """
    digits_reversed = (
        x % base
        for x in while_not(
            lambda x: x == 0,
            accumulate(repeat(value), lambda x, y: x//base)
        )
    )
    return list(reversed(list(digits_reversed)))

def accumulating_collatz(start: int) -> Iterator[int]:
    """
    >>> list(accumulating_collatz(12))
    [12, 6, 3, 10, 5, 16, 8, 4, 2]
    """

    def syracuse(n: int) -> int:
        if n % 2 == 0:
            return n // 2
        return 3*n+1

    return while_not(
        lambda x: x == 1,
        accumulate(repeat(start), lambda a, b: syracuse(a))
    )

from Chapter04.ch04_ex1 import legs, haversine
from Chapter07.ch07_ex1 import Leg
from typing import List, Tuple
def quartiles(trip: List[Leg]) -> List[int]:
    """
    >>> from Chapter07.ch07_ex1 import get_trip
    >>> trip = get_trip()
    >>> quartile = quartiles(trip)
    >>> len(quartile)
    73
    >>> quartile  # doctest: +NORMALIZE_WHITESPACE
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
     1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
     2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
     3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3]
    """
    #print( trip[:2], trip[-1] )
    distances = (leg.distance for leg in trip)
    distance_accum = tuple(accumulate(distances))
    total = distance_accum[-1]+1.0
    quartiles = list(int(4*d/total) for d in distance_accum)
    #print( list(quartiles[a:a+16] for a in range(0,len(quartiles),16)) )
    return quartiles

from contextlib import ExitStack
import csv
def row_iter_csv_tab(*filenames: str) -> Iterator[List[str]]:
    """
    >>> filenames = "Anscombe.txt", "crayola.gpl"
    >>> data= list( row_iter_csv_tab(*filenames) )
    >>> len(data)
    151
    >>> data[0]
    ["Anscombe's quartet"]
    >>> data[14]
    ['GIMP Palette']
    """
    with ExitStack() as stack:
        files: List[TextIO] = [
            stack.enter_context(cast(TextIO, open(name, 'r')))
            for name in filenames
        ]
        # readers = [csv.reader(f, delimiter='\t') for f in files]
        readers = map(lambda f: csv.reader(f, delimiter='\t'), files)
        yield from chain(*readers)

grouping_A = """
>>> from Chapter07.ch07_ex1 import get_trip
>>> trip= get_trip()
>>> quartile= quartiles(trip)
>>> group_iter= groupby( zip( quartile, trip ), key= lambda q_raw: q_raw[0] )
>>> for group_key, group_iter in group_iter:
...    print( "Group", group_key+1, len(list(group_iter)) )
Group 1 23
Group 2 14
Group 3 19
Group 4 17
"""

from collections import defaultdict
from typing import Iterable, Callable, Tuple, List, Dict
D_ = TypeVar("D_")
K_ = TypeVar("K_")
def groupby_2(
        iterable: Iterable[D_],
        key: Callable[[D_], K_]
    ) -> Iterator[Tuple[K_, Iterator[D_]]]:
    groups: Dict[K_, List[D_]] = defaultdict(list)
    for item in iterable:
        groups[key(item)].append(item)
    for g in groups:
        yield g, iter(groups[g])

grouping_B = """
>>> from Chapter07.ch07_ex1 import get_trip
>>> trip= get_trip()
>>> quartile= quartiles(trip)
>>> group_iter= groupby_2( zip( quartile, trip ), key= lambda q_raw: q_raw[0] )
>>> for group_key, group_iter in group_iter:
...     print( "Group", group_key+1, len(list(group_iter)) )
Group 1 23
Group 2 14
Group 3 19
Group 4 17
"""

islicing_A = """
>>> from Chapter03.ch03_ex3 import parse_g
>>> with open("1000.txt") as source:
...    flat= list(parse_g(source))

Groups of five
>>> slices= [flat[i::5] for i in range(5)]
>>> fives= list(zip(*slices))
>>> fives[:2]
[(2, 3, 5, 7, 11), (13, 17, 19, 23, 29)]
>>> fives[-1]
(7879, 7883, 7901, 7907, 7919)

Pairs
>>> pairs = list(zip(flat[0::2], flat[1::2]))
>>> len(pairs)
500
>>> pairs[:3]
[(2, 3), (5, 7), (11, 13)]
>>> pairs[-3:]
[(7877, 7879), (7883, 7901), (7907, 7919)]

>>> flat_iter_1 = iter(flat)
>>> flat_iter_2 = iter(flat)
>>> pairs = list(zip(
...     islice(flat_iter_1, 0, None, 2),
...     islice(flat_iter_2, 1, None, 2))
... )
>>> len(pairs)
500
>>> pairs[:3]
[(2, 3), (5, 7), (11, 13)]
>>> pairs[-3:]
[(7877, 7879), (7883, 7901), (7907, 7919)]

Legs
>>> flat_iter_1= iter(flat)
>>> flat_iter_2= iter(flat)
>>> pairs= list(zip( islice(flat_iter_1, 0, None, 1), islice(flat_iter_2, 1, None, 1) ) )
>>> len(pairs)
999
>>> pairs[:3]
[(2, 3), (3, 5), (5, 7)]
>>> pairs[-3:]
[(7883, 7901), (7901, 7907), (7907, 7919)]

"""

dropping_A = """
>>> import csv
>>> with open("crayola.gpl") as source:
...     rdr= csv.reader( source, delimiter='\\t' )
...     rows = dropwhile( lambda row: row[0] != '#', rdr )
...     color_rows = islice( rows, 1, None )
...     colors = list( (color.split(), name) for color, name in color_rows )
>>> len(colors)
133
>>> colors[0]
(['239', '222', '205'], 'Almond')
>>> colors[-1]
(['255', '174', '66'], 'Yellow Orange')
"""

from Chapter07.ch07_ex1 import float_lat_lon, Leg, Point
from Chapter06.ch06_ex3 import row_iter_kml
from Chapter04.ch04_ex1 import legs, haversine
import urllib.request
from typing import List, Callable

def get_trip_starmap(url: str) -> List[Leg]:
    """
    >>> trip= get_trip_starmap( "file:./Winter%202012-2013.kml" )
    >>> len( trip )
    73
    >>> trip[0]  # doctest: +NORMALIZE_WHITESPACE
    Leg(start=Point(latitude=37.54901619777347, longitude=-76.33029518659048),
     end=Point(latitude=37.840832, longitude=-76.273834),
     distance=17.724564798884984)
    >>> trip[-1]  # doctest: +NORMALIZE_WHITESPACE
    Leg(start=Point(latitude=38.330166, longitude=-76.458504),
     end=Point(latitude=38.976334, longitude=-76.473503),
     distance=38.801864781785845)
    """
    make_leg: Callable[[Point, Point], Leg] = (
        lambda start, end:
        Leg(start, end, haversine(start, end))
    )
    with urllib.request.urlopen(url) as source:
        path_iter = float_lat_lon(
            row_iter_kml(cast(TextIO, source))
        )
        pair_iter = legs(path_iter)
        trip = list(starmap(make_leg, pair_iter))
    return trip

from typing import TextIO, cast, Any
def teeing_A():
    """
    >>> teeing_A() # doctest: +ELLIPSIS
    9.0 7.500...
    """
    import csv
    def mean(iterator: Iterator[float]) -> float:
        it0, it1 = tee(iterator, 2)
        N = sum(1 for x in it0)
        s1 = sum(x for x in it1)
        return s1/N
    def number(x: Any) -> bool:
        try:
            float(x)
            return True
        except ValueError:
            return False
    def get_data(filename: str = "Anscombe.txt") -> List[Tuple[float, ...]]:
        with open(filename) as source:
            rdr = csv.reader(cast(TextIO, source), delimiter='\t')
            data_rows = dropwhile(lambda row: not all(map(number, row)), rdr)
            float_rows = map(lambda row: tuple(map(float, row)), data_rows)
            return list(float_rows)
    data = get_data()
    x_I = (row[0] for row in data)
    y_I = (row[1] for row in data)
    print(mean(x_I), mean(y_I))

__test__ = {
    "grouping_A": grouping_A,
    "grouping_B": grouping_B,
    "islicing_A": islicing_A,
    "dropping_A": dropping_A,
}

def test():
    import doctest
    doctest.testmod(verbose=1)

if __name__ == "__main__":
    test()
