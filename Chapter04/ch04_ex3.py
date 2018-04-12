#!/usr/bin/env python3
"""Functional Python Programming

Chapter 4, Example Set 3
"""


test_map = """
>>> from Chapter04.ch04_ex1 import (
...     float_from_pair, float_lat_lon, row_iter_kml, limits, haversine, legs
... )
>>> import urllib.request
>>> with urllib.request.urlopen("file:./Winter%202012-2013.kml") as source:
...    path= tuple(float_from_pair(float_lat_lon(row_iter_kml(source))))
...    trip= tuple( (start, end, round(haversine(start, end),4))
...        for start,end in legs(iter(path)))

>>> distances1= tuple(map( lambda s_e: (s_e[0], s_e[1], haversine(*s_e)),
...    zip(path, path[1:]) ))

>>> len(distances1)
73
>>> distances1[0]
((37.54901619777347, -76.33029518659048), (37.840832, -76.273834), 17.724564798884984)
>>> distances1[-1]
((38.330166, -76.458504), (38.976334, -76.473503), 38.801864781785845)

>>> distances2= tuple(map( lambda s, e: (s, e, haversine(s, e)), path, path[1:] ))

>>> len(distances2)
73
>>> distances2[0]
((37.54901619777347, -76.33029518659048), (37.840832, -76.273834), 17.724564798884984)
>>> distances2[-1]
((38.330166, -76.458504), (38.976334, -76.473503), 38.801864781785845)

"""

__test__ = {
    "map_tests": test_map,
}

def test():
    import doctest
    doctest.testmod(verbose=1)

if __name__ == "__main__":
    test()
