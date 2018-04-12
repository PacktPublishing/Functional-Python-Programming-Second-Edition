#!/usr/bin/env python3
"""Functional Python Programming

Chapter 7, Example Set 1
"""
# pylint: disable=wrong-import-position,wrong-import-order,too-few-public-methods

from Chapter06.ch06_ex3 import row_iter_kml
from Chapter04.ch04_ex1 import legs, haversine

import urllib.request

first_leg = ((29.050501, -80.651169), (27.186001, -80.139503), 115.1751)

selectors = '''
>>> from typing import Tuple, Callable
>>> Point = Tuple[float, float]
>>> Leg = Tuple[Point, Point, float]
>>> start: Callable[[Leg], Point] = lambda leg: leg[0]
>>> end: Callable[[Leg], Point] = lambda leg: leg[1]
>>> distance = lambda leg: leg[2]
>>> latitude = lambda pt: pt[0]
>>> longitude = lambda pt: pt[1]

>>> first_leg = ((29.050501, -80.651169), (27.186001, -80.139503), 115.1751)
>>> latitude(start(first_leg))
29.050501

>>> start: Callable[[Leg], Point] = lambda leg: leg[0]
>>> latitude(start(first_leg))
29.050501

'''

selectors_args = """
>>> from typing import Tuple, Callable
>>> Point = Tuple[float, float]
>>> Leg = Tuple[Point, Point, float]
>>> start: Callable[[Point, Point, float], Point] = lambda start, end, distance: start
>>> end: Callable[[Point, Point, float], Point] = lambda start, end, distance: end
>>> distance = lambda start, end, distance: distance
>>> latitude = lambda lat, lon: lat
>>> longitude = lambda lat, lon: lon

>>> first_leg = ((29.050501, -80.651169), (27.186001, -80.139503), 115.1751)
>>> latitude(*start(*first_leg)) 
29.050501
"""

# from collections import namedtuple
# Leg = namedtuple("Leg", ("start", "end", "distance"))
# Point = namedtuple("Point", ("latitude", "longitude"))

from typing import NamedTuple

class Point(NamedTuple):
    latitude: float
    longitude: float

class Leg(NamedTuple):
    start: Point
    end: Point
    distance: float

first_leg = Leg(
    Point(29.050501, -80.651169),
    Point(27.186001, -80.139503),
    115.1751
)

named_tuples = """
>>> first_leg = Leg(
...     Point(29.050501, -80.651169),
...     Point(27.186001, -80.139503),
...     115.1751)
>>> first_leg.start.latitude
29.050501
"""

from typing import Tuple, Iterator, List

# pylint: disable=unused-argument
def pick_lat_lon(lon: str, lat: str, alt: str) -> Tuple[str, str]:
    return lat, lon

def float_lat_lon(
        row_iter: Iterator[List[str]]
    ) -> Iterator[Point]:
    return (
        Point(*map(float, pick_lat_lon(*row)))
        for row in row_iter
    )

import codecs
from typing import cast, TextIO, BinaryIO
source = "file:./Winter%202012-2013.kml"
def get_trip(url: str = source) -> List[Leg]:
    with urllib.request.urlopen(url) as source:
        path_iter = float_lat_lon(row_iter_kml(
            # cast(TextIO, source)
            cast(
                TextIO,
                codecs.getreader('utf-8')(cast(BinaryIO, source))
            )
        ))
        pair_iter = legs(path_iter)
        trip_iter = (
            Leg(start, end, round(haversine(start, end), 4))
            for start, end in pair_iter
        )
        trip = list(trip_iter)
    return trip

find_given_leg_demo = """
>>> trip= get_trip()
>>> leg= next(filter(lambda leg: int(leg.distance)==115, trip))
>>> leg.start.latitude
29.050501
"""

__test__ = {
    'selectors': selectors,
    'selectors_args': selectors_args,
    'named_tuples': named_tuples,
    'find_given_leg_demo': find_given_leg_demo,
}

def test():
    import doctest
    doctest.testmod(verbose=1)

if __name__ == "__main__":
    test()
