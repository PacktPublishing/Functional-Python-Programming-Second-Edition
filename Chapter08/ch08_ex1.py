#!/usr/bin/env python3
"""Functional Python Programming

Chapter 8, Example Set 1
"""
# pylint: disable = wrong-import-position,wrong-import-order,too-few-public-methods,missing-docstring

from Chapter04.ch04_ex1 import haversine

#from collections import namedtuple
#Leg = namedtuple("Leg", ("order", "start", "end", "distance"))
#Point = namedtuple("Point", ("latitude", "longitude"))

from typing import NamedTuple
class Point(NamedTuple):
    latitude: float
    longitude: float

class Leg(NamedTuple):
    order: int
    start: Point
    end: Point
    distance: float

from typing import Tuple
def pick_lat_lon(lon: str, lat: str, alt: str) -> Tuple[str, str]:
    return lat, lon

from typing import Iterator, List
def float_lat_lon(row_iter: Iterator[List[str]]) -> Iterator[Point]:
    return (
        Point(*map(float, pick_lat_lon(*row)))
        for row in row_iter
    )

def ordered_leg_iter(
        pair_iter: Iterator[Tuple[Point, Point]]
    ) -> Iterator[Leg]:
    for order, pair in enumerate(pair_iter):
        start, end = pair
        yield Leg(
            order,
            start,
            end,
            round(haversine(start, end), 4)
        )

test_parser = """
>>> from Chapter06.ch06_ex3 import row_iter_kml
>>> from Chapter04.ch04_ex1 import legs, haversine
>>> import urllib.request

>>> filename = "file:./Winter%202012-2013.kml"
>>> with urllib.request.urlopen(filename) as source:
...    path_iter = float_lat_lon(row_iter_kml(source))
...    pair_iter = legs(path_iter)
...    trip_iter = ordered_leg_iter( pair_iter )
...    trip = list(trip_iter)

>>> len(trip)
73
>>> trip[0]
Leg(order=0, start=Point(latitude=37.54901619777347, longitude=-76.33029518659048), end=Point(latitude=37.840832, longitude=-76.273834), distance=17.7246)
>>> trip[-1]
Leg(order=72, start=Point(latitude=38.330166, longitude=-76.458504), end=Point(latitude=38.976334, longitude=-76.473503), distance=38.8019)

"""

__test__ = {
    "test_parser": test_parser,
}

def test():
    import doctest
    doctest.testmod(verbose=True)

if __name__ == "__main__":
    test()
