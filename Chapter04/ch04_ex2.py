#!/usr/bin/env python3
"""Functional Python Programming

Chapter 4, Example Set 2
Also used in Chapter 5.
"""
# pylint: disable=line-too-long,wrong-import-position,reimported

from typing import Iterable, Tuple, Any

Wrapped = Tuple[Any, Tuple]
def wrap(leg_iter: Iterable[Tuple]) -> Iterable[Wrapped]:
    return ((leg[2], leg) for leg in leg_iter)

def unwrap(dist_leg: Tuple[Any, Any]) -> Any:
    # pylint: disable=unused-variable
    distance, leg = dist_leg
    return leg

def by_dist(leg: Tuple[Any, Any, Any]) -> Any:
    # pylint: disable=unused-variable
    lat, lon, dist = leg
    return dist

test_max_alternatives = """
>>> from Chapter04.ch04_ex1 import (
...     float_from_pair, float_lat_lon, row_iter_kml, limits, legs,
...     haversine)
>>> import urllib.request
>>> with urllib.request.urlopen("file:./Winter%202012-2013.kml") as source:
...    path= float_from_pair(float_lat_lon(row_iter_kml(source)))
...    trip= tuple( (start, end, round(haversine(start, end),4))
...        for start,end in legs(path))

>>> long = max(dist for start, end, dist in trip)
>>> short = min(dist for start, end, dist in trip)
>>> long
129.7748
>>> short
0.1731

>>> long, short = unwrap( max( wrap( trip ) ) ), unwrap( min( wrap( trip ) ) )
>>> long
((27.154167, -80.195663), (29.195168, -81.002998), 129.7748)
>>> short
((35.505665, -76.653664), (35.508335, -76.654999), 0.1731)

>>> long, short = max(trip, key=by_dist), min(trip, key=by_dist)
>>> long
((27.154167, -80.195663), (29.195168, -81.002998), 129.7748)
>>> short
((35.505665, -76.653664), (35.508335, -76.654999), 0.1731)
"""

from typing import Iterable, Any, Callable
def max_like(trip: Iterable[Any], key: Callable=lambda x: x) -> Any:
    """
    >>> max_like([1, 3, 2])
    3
    """
    wrapped = ((key(leg), leg) for leg in trip)
    return sorted(wrapped)[-1][1]


start = lambda x: x[0]
end = lambda x: x[1]
dist = lambda x: x[2]

lat = lambda x: x[0]
lon = lambda x: x[1]

test_min_max = """
>>> from Chapter04.ch04_ex1 import (
...     float_from_pair, float_lat_lon, row_iter_kml, limits, legs,
...     haversine)
>>> import urllib.request
>>> with urllib.request.urlopen("file:./Winter%202012-2013.kml") as source:
...    path= float_from_pair(float_lat_lon(row_iter_kml(source)))
...    trip= tuple( (start, end, round(haversine(start, end),4))
...        for start,end in legs(path))

>>> long, short = max(trip, key=dist), min(trip, key=dist)
>>> long
((27.154167, -80.195663), (29.195168, -81.002998), 129.7748)
>>> short
((35.505665, -76.653664), (35.508335, -76.654999), 0.1731)

>>> north = min( trip, key=lambda x: lat(start(x)) )
>>> north
((23.9555, -76.31633), (24.099667, -76.401833), 9.844)

"""

test_conversion = """
>>> from Chapter04.ch04_ex1 import (
...     float_from_pair, float_lat_lon, row_iter_kml, limits, legs,
...     haversine)
>>> import urllib.request
>>> with urllib.request.urlopen("file:./Winter%202012-2013.kml") as source:
...    path= float_from_pair(float_lat_lon(row_iter_kml(source)))
...    trip= tuple( (start, end, round(haversine(start, end),4))
...        for start,end in legs(path))

>>> statute1 = list( (start(x),end(x),dist(x)*6076.12/5280) for x in trip )
>>> statute2 = list( map( lambda x: (start(x),end(x),dist(x)*6076.12/5280), trip ) )
>>> statute3 = list( (b, e, d*6076.12/5280) for b, e, d in trip )

>>> assert statute1 == statute2
>>> assert statute1 == statute3

>>> statute1[0]
((37.54901619777347, -76.33029518659048), (37.840832, -76.273834), 20.397120559090908)

>>> statute1[-1]
((38.330166, -76.458504), (38.976334, -76.473503), 44.652462240151515)

"""

test_filter_sorted = """
>>> from Chapter04.ch04_ex1 import (
...     float_from_pair, float_lat_lon, row_iter_kml, limits, legs,
...     haversine)
>>> import urllib.request
>>> with urllib.request.urlopen("file:./Winter%202012-2013.kml") as source:
...    path= float_from_pair(float_lat_lon(row_iter_kml(source)))
...    trip= tuple( (start, end, round(haversine(start, end),4))
...        for start,end in legs(path))

>>> long= list(filter( lambda leg: dist(leg) >= 50, trip ))
>>> len(long)
14
>>> long[0]
((34.204666, -77.800499), (33.276833, -78.979332), 81.0363)
>>> long[-1]
((31.9105, -80.780998), (32.83248254681784, -79.93379468285697), 70.0694)

>>> s1= sorted( dist(x) for x in trip)
>>> s1[0]
0.1731
>>> s1[-1]
129.7748

>>> s2=( sorted( trip, key=dist ) )
>>> s2[0]
((35.505665, -76.653664), (35.508335, -76.654999), 0.1731)
>>> s2[-1]
((27.154167, -80.195663), (29.195168, -81.002998), 129.7748)

>>> from Chapter04.ch04_ex4 import mean, stdev, z

>>> dist_data = list(map(dist, trip))
>>> μ_d = mean(dist_data)
>>> σ_d = stdev(dist_data)
>>> print( "Average leg", μ_d, "with σ_d of", σ_d, "Z(0)=", z(0,μ_d,σ_d) )
Average leg 33.99131780821918 with σ_d of 24.158473730346035 Z(0)= -1.407014291864054

>>> outlier = lambda leg: abs(z(dist(leg),μ_d,σ_d)) > 3
>>> print( "Outliers", list( filter( outlier, trip ) ) )
Outliers [((29.050501, -80.651169), (27.186001, -80.139503), 115.1751), ((27.154167, -80.195663), (29.195168, -81.002998), 129.7748)]
"""

def performance():
    print(
        "map",
        timeit.timeit(
            """list(map(int,data))""",
            """data = ['2', '3', '5', '7', '11', '13', '17', '19', '23', '29', '31', '37', '41', '43', '47', '53', '59', '61', '67', '71', '73', '79', '83', '89', '97', '101', '103', '107', '109', '113', '127', '131', '137', '139', '149', '151', '157', '163', '167', '173', '179', '181', '191', '193', '197', '199', '211', '223', '227', '229']"""
        )
    )
    print(
        "expr",
        timeit.timeit(
            """list(int(v) for v in data)""",
            """data = ['2', '3', '5', '7', '11', '13', '17', '19', '23', '29', '31', '37', '41', '43', '47', '53', '59', '61', '67', '71', '73', '79', '83', '89', '97', '101', '103', '107', '109', '113', '127', '131', '137', '139', '149', '151', '157', '163', '167', '173', '179', '181', '191', '193', '197', '199', '211', '223', '227', '229']"""
        )
    )


__test__ = {
    "test_max_alternatives": test_max_alternatives,
    "test_min_max": test_min_max,
    "test_conversion": test_conversion,
    "test_filter_sorted": test_filter_sorted,
}

def test():
    import doctest
    doctest.testmod(verbose=1)

if __name__ == "__main__":
    # import timeit
    # performance()
    test()
