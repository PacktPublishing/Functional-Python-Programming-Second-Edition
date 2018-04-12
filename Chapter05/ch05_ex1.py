#!/usr/bin/env python3
"""Functional Python Programming

Chapter 5, Example Set 1
"""
# pylint: disable=reimported,wrong-import-position

from typing import Callable, Iterable, Tuple, Iterator, Any
Conv_F = Callable[[float], float]
Leg = Tuple[Any, Any, float]
def convert(conversion: Conv_F, trip: Iterable[Leg]) -> Iterator[float]:
    return (conversion(distance) for start, end, distance in trip)

to_miles = lambda nm: nm*6076.12/5280
to_km = lambda nm: nm*1.852
to_nm = lambda nm: nm

fst = lambda x: x[0]
snd = lambda x: x[1]
sel2 = lambda x: x[2]

to_miles_sel2 = lambda s_e_d: to_miles(sel2(s_e_d))

test_convert = """
>>> from Chapter04.ch04_ex1 import (
...    float_from_pair, float_lat_lon, row_iter_kml, limits, haversine, legs
... )
>>> import urllib.request
>>> data = "file:./Winter%202012-2013.kml"
>>> with urllib.request.urlopen(data) as source:
...     path= float_from_pair(float_lat_lon(row_iter_kml(source)))
...     trip= tuple( (start, end, round(haversine(start, end), 4))
...         for start, end in legs(path))

>>> trip[0]
((37.54901619777347, -76.33029518659048), (37.840832, -76.273834), 17.7246)
>>> trip[-1]
((38.330166, -76.458504), (38.976334, -76.473503), 38.8019)

>>> miles= list( convert( to_miles, trip ) )
>>> miles[0]
20.397120559090908
>>> miles[-1]
44.652462240151515

>>> miles2 = list( to_miles_sel2(s_e_d) for s_e_d in trip )
>>> miles2[0]
20.397120559090908
>>> miles2[-1]
44.652462240151515

>>> assert miles == miles2
"""

from typing import Callable, Iterable, Tuple, Iterator, Any
Point = Tuple[float, float]
Leg_Raw = Tuple[Point, Point]
Point_Func = Callable[[Point, Point], float]
Leg_D = Tuple[Point, Point, float]

def cons_distance(
        distance: Point_Func,
        legs_iter: Iterable[Leg_Raw]
    ) -> Iterator[Leg_D]:
    return (
        (start, end, round(distance(start, end), 4))
        for start, end in legs_iter
    )

test_cons_distance = """
>>> from Chapter04.ch04_ex1 import (
...    float_from_pair, float_lat_lon, row_iter_kml, limits, haversine, legs
... )
>>> import urllib.request
>>> with urllib.request.urlopen("file:./Winter%202012-2013.kml") as source:
...    path= float_from_pair(float_lat_lon(row_iter_kml(source)))
...    trip2= tuple( cons_distance( haversine, legs(iter(path)) ) )

>>> trip2[0]
((37.54901619777347, -76.33029518659048), (37.840832, -76.273834), 17.7246)
>>> trip2[-1]
((38.330166, -76.458504), (38.976334, -76.473503), 38.8019)

"""

from typing import Callable, Iterable, Tuple, Iterator, Any
Point = Tuple[float, float]
Leg_Raw = Tuple[Point, Point]
Point_Func = Callable[[Point, Point], float]
Leg_P_D = Tuple[Leg_Raw, ...]

def cons_distance3(
        distance: Point_Func,
        legs_iter: Iterable[Leg_Raw]) -> Iterator[Leg_P_D]:
    return (
        leg+(round(distance(*leg), 4),)  # 1-tuple
        for leg in legs_iter
    )

test_cons_distance3 = """
>>> from Chapter04.ch04_ex1 import (
...    float_from_pair, float_lat_lon, row_iter_kml, limits, haversine, legs
... )
>>> import urllib.request
>>> with urllib.request.urlopen("file:./Winter%202012-2013.kml") as source:
...    path= float_from_pair(float_lat_lon(row_iter_kml(source)))
...    trip3= tuple( cons_distance3( haversine, legs(iter(path)) ) )

>>> trip3[0]
((37.54901619777347, -76.33029518659048), (37.840832, -76.273834), 17.7246)
>>> trip3[-1]
((38.330166, -76.458504), (38.976334, -76.473503), 38.8019)

"""

from typing import Callable, Iterator
Num_Conv = Callable[[str], float]
def numbers_from_rows(conversion: Num_Conv, text: str) -> Iterator[float]:
    return (
        conversion(value)
        for line in text.splitlines()
        for value in line.split()
    )

test_numbers_from_rows = """
>>> text= '''      2      3      5      7     11     13     17     19     23     29
...     31     37     41     43     47     53     59     61     67     71
...    179    181    191    193    197    199    211    223    227    229'''

>>> list(numbers_from_rows( float, text ) )
[2.0, 3.0, 5.0, 7.0, 11.0, 13.0, 17.0, 19.0, 23.0, 29.0, 31.0, 37.0, 41.0, 43.0, 47.0, 53.0, 59.0, 61.0, 67.0, 71.0, 179.0, 181.0, 191.0, 193.0, 197.0, 199.0, 211.0, 223.0, 227.0, 229.0]

"""

def group_by_iter(n: int, items: Iterator) -> Iterator[Tuple]:
    """
    >>> list( group_by_iter( 7, filter( lambda x: x%3==0 or x%5==0, range(1,50) ) ) )
    [(3, 5, 6, 9, 10, 12, 15), (18, 20, 21, 24, 25, 27, 30), (33, 35, 36, 39, 40, 42, 45), (48,)]
    """
    row = tuple(next(items) for i in range(n))
    while row:
        yield row
        row = tuple(next(items) for i in range(n))


def group_filter_iter(n: int, pred: Callable, items: Iterator) -> Iterator:
    """
    >>> list( group_filter_iter( 7, lambda x: x%3==0 or x%5==0, range(1,50) ) )
    [(3, 5, 6, 9, 10, 12, 15), (18, 20, 21, 24, 25, 27, 30), (33, 35, 36, 39, 40, 42, 45), (48,)]
    """
    subset = filter(pred, items)
    row = tuple(next(subset) for i in range(n))
    while row:
        yield row
        row = tuple(next(subset) for i in range(n))

def sum_filter_f(filter_f: Callable, function: Callable, data: Iterable) -> Iterator:
    return sum(function(x) for x in data if filter_f(x))

count_ = lambda x: 1
sum_ = lambda x: x
valid = lambda x: x is not None

test_sum_filter_f = """
>>> text= '''      2      3      5      7     11     13     17     19     23     29
...     31     37     41     43     47     53     59     61     67     71
...    179    181    191    193    197    199    211    223    227    229'''

>>> data= tuple(numbers_from_rows( int, text ))
>>> len(data)
30

>>> sum_filter_f( valid, count_, data )
30
>>> sum_filter_f( valid, sum_, data )
2669
"""

def first(predicate: Callable, collection: Iterable) -> Any:
    for x in collection:
        if predicate(x):
            return x

import math
def isprimeh(x: int) -> bool:
    """
    >>> tuple( isprimeh(x) for x in range(3,11) )
    (True, False, True, False, True, False, False, False)
    """
    if x == 2:
        return True
    if x % 2 == 0:
        return False
    factor = first(lambda n: x%n == 0, range(3, int(math.sqrt(x)+.5)+1, 2))
    return factor is None

def map_not_none(func: Callable, source: Iterable) -> Iterator:
    """
    >>> list( map_not_none( lambda x:x**2, [1, 2, 3, None, 4.5] ) )
    [1, 4, 9, 20.25]
    """
    for x in source:
        try:
            yield func(x)
        except Exception as e:  # pylint: disable=broad-except,unused-variable
            pass # print(e)


__test__ = {
    "test_convert": test_convert,
    "test_cons_distance": test_cons_distance,
    "test_cons_distance3": test_cons_distance3,
    "test_numbers_from_rows": test_numbers_from_rows,
    "test_sum_filter_f": test_sum_filter_f,
}

def test():
    import doctest
    doctest.testmod(verbose=1)

if __name__ == "__main__":
    test()
