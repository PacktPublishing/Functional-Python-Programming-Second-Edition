#!/usr/bin/env python3
"""Functional Python Programming

Chapter 6, Example Set 2
"""
# pylint: disable=reimported,wrong-import-position

from collections import defaultdict

from typing import Callable, Sequence, Dict, List, TypeVar
S_ = TypeVar("S_")
K_ = TypeVar("K_")
def group_by(key: Callable[[S_], K_], data: Sequence[S_]) -> Dict[K_, List[S_]]:
    def group_into(
            key: Callable[[S_], K_],
            collection: Sequence[S_],
            dictionary: Dict[K_, List[S_]]
        ) -> Dict[K_, List[S_]]:
        if len(collection) == 0:
            return dictionary
        head, *tail = collection
        dictionary[key(head)].append(head)
        return group_into(key, tail, dictionary)
    return group_into(key, data, defaultdict(list))

binned_distance = lambda leg: 5*(leg[2]//5)

test_group_by = """
>>> from Chapter04.ch04_ex1 import (
...    float_from_pair, float_lat_lon, row_iter_kml, limits, haversine, legs
... )
>>> import urllib.request
>>> with urllib.request.urlopen("file:./Winter%202012-2013.kml") as source:
...    path= float_from_pair(float_lat_lon(row_iter_kml(source)))
...    trip= tuple( (start, end, round(haversine(start, end),4))
...        for start,end in legs(path))

>>> by_distance= group_by(binned_distance, trip)
>>> for distance in sorted(by_distance):
...     print( distance, len(by_distance[distance]) )
0.0 4
5.0 5
10.0 5
15.0 9
20.0 5
25.0 5
30.0 15
35.0 5
40.0 3
45.0 3
50.0 3
55.0 1
60.0 3
65.0 1
70.0 2
80.0 1
85.0 1
115.0 1
125.0 1
"""

from typing import Callable, Iterable, Dict, List
def partition(
        key: Callable[[S_], K_],
        data: Iterable[S_]
    ) -> Dict[K_, List[S_]]:
    dictionary: Dict[K_, List[S_]] = defaultdict(list)
    for head in data:
        dictionary[key(head)].append(head)
    return dictionary


test_partition = """
>>> from Chapter04.ch04_ex1 import (
...    float_from_pair, float_lat_lon, row_iter_kml, limits, haversine, legs
... )
>>> import urllib.request
>>> with urllib.request.urlopen("file:./Winter%202012-2013.kml") as source:
...    path= float_from_pair(float_lat_lon(row_iter_kml(source)))
...    trip= tuple( (start, end, round(haversine(start, end),4))
...        for start,end in legs(path))

>>> by_distance= partition(binned_distance, trip)
>>> for distance in sorted(by_distance):
...    print( distance, len(by_distance[distance]) )
0.0 4
5.0 5
10.0 5
15.0 9
20.0 5
25.0 5
30.0 15
35.0 5
40.0 3
45.0 3
50.0 3
55.0 1
60.0 3
65.0 1
70.0 2
80.0 1
85.0 1
115.0 1
125.0 1
"""

start = lambda s, e, d: s
end = lambda s, e, d: e
dist = lambda s, e, d: d
latitude = lambda lat, lon: lat
longitude = lambda lat, lon: lon

test_sorted_max = """
>>> from Chapter04.ch04_ex1 import (
...    float_from_pair, float_lat_lon, row_iter_kml, limits, haversine, legs
... )
>>> import urllib.request
>>> with urllib.request.urlopen("file:./Winter%202012-2013.kml") as source:
...    path= float_from_pair(float_lat_lon(row_iter_kml(source)))
...    trip= tuple( (start, end, round(haversine(start, end),4))
...        for start,end in legs(path))

>>> by_distance= partition(binned_distance, trip)
>>> for distance in sorted(by_distance):
...    print( distance, max(by_distance[distance], key=lambda pt: latitude(*start(*pt)) ) )
0.0 ((35.505665, -76.653664), (35.508335, -76.654999), 0.1731)
5.0 ((38.845501, -76.537331), (38.992832, -76.451332), 9.7151)
10.0 ((36.444168, -76.3265), (36.297501, -76.217834), 10.2537)
15.0 ((37.840332, -76.27417), (37.547165, -76.32917), 17.7944)
20.0 ((37.547165, -76.32917), (37.181168, -76.411499), 22.3226)
25.0 ((36.297501, -76.217834), (35.935501, -75.939331), 25.5897)
30.0 ((38.331501, -76.459503), (38.845501, -76.537331), 31.0756)
35.0 ((38.992832, -76.451332), (38.331165, -76.459167), 39.7277)
40.0 ((36.843334, -76.298668), (37.549, -76.331169), 42.3962)
45.0 ((37.549, -76.331169), (38.330166, -76.458504), 47.2866)
50.0 ((33.276833, -78.979332), (32.832169, -79.93383), 54.9528)
55.0 ((31.1595, -81.421997), (31.9105, -80.780998), 55.7582)
60.0 ((29.887167, -81.30883), (29.050501, -80.651169), 60.8693)
65.0 ((31.671333, -80.933167), (30.717167, -81.552498), 65.5252)
70.0 ((31.9105, -80.780998), (32.83248254681784, -79.93379468285697), 70.0694)
80.0 ((34.204666, -77.800499), (33.276833, -78.979332), 81.0363)
85.0 ((32.832169, -79.93383), (31.671333, -80.933167), 86.2095)
115.0 ((29.050501, -80.651169), (27.186001, -80.139503), 115.1751)
125.0 ((27.154167, -80.195663), (29.195168, -81.002998), 129.7748)
"""

__test__ = {
    "test_group_by": test_group_by,
    "test_partition": test_partition,
    "test_sorted_max": test_sorted_max,
}

def test():
    import doctest
    doctest.testmod(verbose=1)

if __name__ == "__main__":
    test()
