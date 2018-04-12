#!/usr/bin/env python3
"""Functional Python Programming

Chapter 6, Example Set 5
"""
#pylint: disable=reimported,wrong-import-position
from typing import Dict, Any, Iterable, Tuple, List, TypeVar

Leg = Tuple[Any, Any, float]
T_ = TypeVar("T_")

def group_sort1(trip: Iterable[Leg]) -> Dict[int, int]:
    """Group legs into bins with distances 5 nm or less.

    >>> trip = [ ('s1', 'e1', 1), ('s4', 'e4', 4.9), ('s5', 'e5', 5), ('s6', 'e6', 6)]
    >>> group_sort1(trip)
    {0: 2, 5: 2}
    """
    def group(
            data: Iterable[T_]
        ) -> Iterable[Tuple[T_, int]]:
        previous, count = None, 0
        for d in sorted(data):
            if d == previous:
                count += 1
            elif previous is not None: # and d != previous
                yield previous, count
                previous, count = d, 1
            elif previous is None:
                previous, count = d, 1
            else:
                raise Exception("Bad bad design problem.")
        yield previous, count
    quantized = (int(5*(dist//5)) for start, stop, dist in trip)
    return dict(group(quantized))

    # return sorted(tuple(group(quantized)),
    #    key=lambda x:x[1], reverse=True )

def group_sort2(trip: Iterable[Leg]) -> Dict[int, int]:
    """Group legs into bins with distances 5 nm or less.

    >>> trip = [ ('s1', 'e1', 1), ('s4', 'e4', 4.9), ('s5', 'e5', 5), ('s6', 'e6', 6)]
    >>> group_sort2(trip)
    {0: 2, 5: 2}
    """
    def group(data: Iterable[T_]) -> Iterable[Tuple[T_, int]]:
        sorted_data = iter(sorted(data))
        previous, count = next(sorted_data), 1
        for d in sorted_data:
            if d == previous:
                count += 1
            elif previous is not None: # and d != previous
                yield previous, count
                previous, count = d, 1
            else:
                raise Exception("Bad bad design problem.")
        yield previous, count
    quantized = (int(5*(dist//5)) for start, stop, dist in trip)
    try:
        return dict(group(quantized))
    except StopIteration:
        return dict()

    # return sorted(tuple(group(quantized)),
    #    key=lambda x:x[1], reverse=True )

from collections import Counter
def group_Counter(trip: Iterable[Leg]) -> List[Tuple[int, int]]:
    """Group legs into bins with distances 5 nm or less.

    >>> trip = [ ('s1', 'e1', 1), ('s4', 'e4', 4.9), ('s5', 'e5', 5), ('s6', 'e6', 6)]
    >>> group_Counter(trip)
    [(0, 2), (5, 2)]
    """
    quantized = (int(5*(dist//5)) for start, stop, dist in trip)
    return Counter(quantized).most_common()

trip1 = """
>>> import urllib.request
>>> from Chapter04.ch04_ex1 import (
...    float_from_pair, float_lat_lon, row_iter_kml, limits, haversine, legs
... )
>>> with urllib.request.urlopen("file:./Winter%202012-2013.kml") as source:
...     trip= tuple( (start, end, round(haversine(start, end),4))
...         for start,end in legs( float_from_pair(float_lat_lon(row_iter_kml(source)))) )
>>> start, end, dist = trip[0]
>>> start, end, dist
((37.54901619777347, -76.33029518659048), (37.840832, -76.273834), 17.7246)
>>> start, end, dist = trip[-1]
>>> start, end, dist
((38.330166, -76.458504), (38.976334, -76.473503), 38.8019)

>>> lat_iter = (lat1 for lat1, lon1 in (start for start,stop,dist in trip) )
>>> north, south = limits( lat_iter )
>>> dist_iter= (dist for start,stop,dist in trip)
>>> total= sum( dist_iter )
>>> average = total/len(trip)

>>> print( "south", south )
south 23.9555
>>> print( "north", north )
north 38.992832
>>> print( "total", total )
total 2481.3662
>>> print( "average", round(average,3) )
average 33.991

>>> expected = {0.0: 4, 65.0: 1, 35.0: 5, 5.0: 5, 70.0: 2, 40.0: 3, 10.0: 5, 45.0: 3, 15.0: 9, 80.0: 1, 50.0: 3, 115.0: 1, 20.0: 5, 85.0: 1, 55.0: 1, 25.0: 5, 60.0: 3, 125.0: 1, 30.0: 15}
>>> group_sort1(trip) == expected
True
>>> print( "Mode1", group_sort1(trip) )
Mode1 {0: 4, 5: 5, 10: 5, 15: 9, 20: 5, 25: 5, 30: 15, 35: 5, 40: 3, 45: 3, 50: 3, 55: 1, 60: 3, 65: 1, 70: 2, 80: 1, 85: 1, 115: 1, 125: 1}

>>> group_sort2(trip) == expected
True
>>> print( "Mode2", group_sort2(trip) )
Mode2 {0: 4, 5: 5, 10: 5, 15: 9, 20: 5, 25: 5, 30: 15, 35: 5, 40: 3, 45: 3, 50: 3, 55: 1, 60: 3, 65: 1, 70: 2, 80: 1, 85: 1, 115: 1, 125: 1}

>>> expected = [(30.0, 15), (15.0, 9), (35.0, 5), (5.0, 5), (10.0, 5), (20.0, 5), (25.0, 5), (0.0, 4), (40.0, 3), (45.0, 3), (50.0, 3), (60.0, 3), (70.0, 2), (65.0, 1), (80.0, 1), (115.0, 1), (85.0, 1), (55.0, 1), (125.0, 1)]
>>> set(group_Counter(trip)) == set(expected)
True
>>> print( "Mode3", group_Counter(trip) )
Mode3 [(30, 15), (15, 9), (5, 5), (35, 5), (20, 5), (10, 5), (25, 5), (0, 4), (50, 3), (60, 3), (45, 3), (40, 3), (70, 2), (80, 1), (85, 1), (65, 1), (115, 1), (125, 1), (55, 1)]

"""

trip2 = """
If we modify this demo so that path is an iterable, not a materialized tuple,
we'll see that the ``limit()`` function doesn't really do what we hoped.

>>> import urllib.request
>>> from Chapter04.ch04_ex1 import (
...    float_from_pair, float_lat_lon, row_iter_kml, limits, haversine, legs
... )
>>> with urllib.request.urlopen("file:./Winter%202012-2013.kml") as source:
...    path= tuple(float_from_pair(float_lat_lon(row_iter_kml(source))))
>>> north, south = limits( path )

>>> trip= tuple( (start, end, round(haversine(start, end),4))
...     for start,end in legs(iter(path)) )

>>> start, end, dist = trip[0]
>>> start, end, dist
((37.54901619777347, -76.33029518659048), (37.840832, -76.273834), 17.7246)
>>> start, end, dist = trip[-1]
>>> start, end, dist
((38.330166, -76.458504), (38.976334, -76.473503), 38.8019)

>>> dist_iter= (dist for start,stop,dist in trip)
>>> total= sum( dist_iter )
>>> average = total/len(trip)

>>> print( "south", south )
south (23.9555, -76.31633)
>>> print( "north", north )
north (38.992832, -76.451332)
>>> print( "total", total )
total 2481.3662
>>> print( "average", round(average,3) )
average 33.991
"""

from typing import Callable, Iterable, Any
def sum_f(function: Callable[[Any], float], data: Iterable) -> float:
    """
    >>> sum_f(lambda x: x//2, [2, 4, 6, 8, 10])
    15
    """
    return sum(function(x) for x in data)

__test__ = {
    'trip1 demo': trip1,
    'trip2 demo': trip2,
}

def test():
    import doctest
    doctest.testmod(verbose=True)

if __name__ == "__main__":
    test()
