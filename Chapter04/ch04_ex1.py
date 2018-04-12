#!/usr/bin/env python3
"""Functional Python Programming

Chapter 4, Example Set 1
"""
# pylint: disable=line-too-long,wrong-import-position,reimported

import urllib.request
import xml.etree.ElementTree as XML
import csv
from typing import Text, List, TextIO, Iterable, Tuple, Iterator

def comma_split(text: Text) -> List[Text]:
    return text.split(",")

def row_iter_kml(file_obj: TextIO) -> Iterable[List[Text]]:
    """Iterate over rows in a KML file.

    >>> import io
    >>> doc= io.StringIO('''<?xml version="1.0" encoding="UTF-8"?>
    ... <kml xmlns="http://www.opengis.net/kml/2.2" xmlns:gx="http://www.google.com/kml/ext/2.2" xmlns:kml="http://www.opengis.net/kml/2.2" xmlns:atom="http://www.w3.org/2005/Atom">
    ... <Document>
    ...	    <Folder>
    ...		<name>Waypoints.kml</name>
    ...		<open>1</open>
    ...		<Placemark>
    ...			<Point>
    ...				<coordinates>-76.33029518659048,37.54901619777347,0</coordinates>
    ...			</Point>
    ...		</Placemark>
    ...    </Folder>
    ... </Document>
    ... </kml>''')
    >>> list(row_iter_kml(doc))
    [['-76.33029518659048', '37.54901619777347', '0']]
    """
    ns_map = {
        "ns0": "http://www.opengis.net/kml/2.2",
        "ns1": "http://www.google.com/kml/ext/2.2"}
    path_to_points = (
        "./ns0:Document/ns0:Folder/ns0:Placemark/"
        "ns0:Point/ns0:coordinates")
    doc = XML.parse(file_obj)
    return (
        comma_split(Text(coordinates.text))
        for coordinates in
        doc.findall(path_to_points, ns_map)
        )

def pick_lat_lon(lon: Text, lat: Text, alt: Text) -> Tuple[Text, Text]:
    return lat, lon

Rows = Iterable[List[Text]]
LL_Text = Tuple[Text, Text]
def lat_lon_kml(row_iter: Rows) -> Iterable[LL_Text]:
    """
    >>> data= [['-76.33029518659048', '37.54901619777347', '0']]
    >>> list(lat_lon_kml( data ))
    [('37.54901619777347', '-76.33029518659048')]
    """
    return (pick_lat_lon(*row) for row in row_iter)

def demo1():
    """
    >>> demo1()  # doctest: +ELLIPSIS
    (('37.54901619777347', '-76.33029518659048'), ..., ('38.976334', '-76.47350299999999'))
    """
    url = "file:./Winter%202012-2013.kml"
    with urllib.request.urlopen(url) as source:
        v1 = tuple(float_lat_lon_a(row_iter_kml(source)))
    print(v1)

def float_lat_lon_a(row_iter: Iterator[List[Text]]) -> Iterable[Tuple[Text, Text]]:
    """
    >>> data= [['-76.33029518659048', '37.54901619777347', '0']]
    >>> list(float_lat_lon_a( data ))
    [('37.54901619777347', '-76.33029518659048')]
    """
    return (
        pick_lat_lon(*row)
        for row in row_iter
    )

def float_lat_lon(row_iter: Iterator[List[Text]]) -> Iterable[Tuple[float, ...]]:
    """
    >>> data= [['-76.33029518659048', '37.54901619777347', '0']]
    >>> list(float_lat_lon( data ))
    [(37.54901619777347, -76.33029518659048)]
    """
    return (
        tuple(map(float, pick_lat_lon(*row)))
        for row in row_iter
    )

def lat_lon_csv(source: TextIO) -> Iterable[List[Text]]:
    """Lat_lon values built from a CSV source.
    """
    rdr = csv.reader(source)
    header = next(rdr)
    return rdr.rows()

from typing import Iterator, Tuple, Text, Iterable
Text_Iter = Iterable[Tuple[Text, Text]]
LL_Iter = Iterable[Tuple[float, float]]
def float_from_pair(lat_lon_iter: Text_Iter) -> LL_Iter:
    """Create float lat-lon pairs from string lat-lon pairs.

    >>> trip = [ ("1", "2"), ("2.718", "3.142") ]
    >>> tuple( float_from_pair( trip ) )
    ((1.0, 2.0), (2.718, 3.142))
    """
    return ((float(lat), float(lon)) for lat, lon in lat_lon_iter)

from typing import Iterator, Any, Iterable, TypeVar
T_ = TypeVar('T_')
Pairs_Iter = Iterator[Tuple[T_, T_]]
def legs(lat_lon_iter: Iterator[T_]) -> Pairs_Iter:
    """We can think of this as yielding list[0:1], list[1:2], list[2:3], ..., list[n-2,n-1]
    Another option is zip( list[0::2], list[1::2] )

    >>> trip = iter([ (0,0), (1,0), (1,1), (0,1), (0,0) ])
    >>> tuple( legs( trip ) )
    (((0, 0), (1, 0)), ((1, 0), (1, 1)), ((1, 1), (0, 1)), ((0, 1), (0, 0)))
    """
    start = next(lat_lon_iter)
    for end in lat_lon_iter:
        yield start, end
        start = end

from typing import Iterator, Tuple, Callable, Iterable
# Pairs_Iter = Iterator[Tuple[float, float]]
Leg = Tuple[Tuple[float, float], Tuple[float, float]]
Leg_Iter = Iterable[Leg]
def legs_filter(
        lat_lon_iter: Pairs_Iter,
        rejection_rule: Callable[[Tuple[float, float], Tuple[float, float]], bool]) -> Leg_Iter:
    """
    >>> trip = iter([ (0,0), (1,0), (2,0), (2,1), (2,2), (0,1), (0,0) ])
    >>> some_rule = lambda b, e: b[0] == 0
    >>> list(legs_filter(trip, some_rule))
    [((1, 0), (2, 0)), ((2, 0), (2, 1)), ((2, 1), (2, 2)), ((2, 2), (0, 1))]
    """
    begin = next(lat_lon_iter)
    for end in lat_lon_iter:
        if rejection_rule(begin, end):
            pass
        else:
            yield begin, end
        begin = end

Item_Iter = Iterator[Any]
# Pairs_Iter = Iterable[Tuple[Any, Any]]
def pairs(iterator: Item_Iter) -> Pairs_Iter:
    """Another way of pairing up values.

    >>> trip = iter([ (0,0), (1,0), (1,1), (0,1), (0,0) ])
    >>> list( pairs( trip ) )
    [((0, 0), (1, 0)), ((1, 0), (1, 1)), ((1, 1), (0, 1)), ((0, 1), (0, 0))]
    """
    def pair_from(head: Any, iterable_tail: Item_Iter) -> Pairs_Iter:
        nxt = next(iterable_tail)
        yield head, nxt
        # Pre Python 3.3
        # for pairs in pair_from( nxt, iterable_tail ):
        #    yield pairs
        # Python 3.3 yield from
        yield from pair_from(nxt, iterable_tail)

    try:
        return pair_from(next(iterator), iterator)
    except StopIteration:
        return iter([])

from math import radians, sin, cos, sqrt, asin
from typing import Tuple

MI = 3959
NM = 3440
KM = 6371

Point = Tuple[float, float]
def haversine(p1: Point, p2: Point, R: float=NM) -> float:
    """Distance between points.
    point1 and point2 are two-tuples of latitude and longitude.
    R is radius, R=MI computes in miles.

    >>> round(haversine((36.12, -86.67), (33.94, -118.40), R=6372.8), 5)
    2887.25995
    """
    lat_1, lon_1 = p1
    lat_2, lon_2 = p2

    D_lat = radians(lat_2 - lat_1)
    D_lon = radians(lon_2 - lon_1)
    lat_1 = radians(lat_1)
    lat_2 = radians(lat_2)

    a = sqrt(sin(D_lat/2)**2 + cos(lat_1)*cos(lat_2)*sin(D_lon/2)**2)
    c = 2*asin(a)

    return R * c

import itertools
from typing import Iterable, TypeVar

# Ideally...
Sortable = TypeVar('Sortable')      # Declare type variable
# However itertools.tee() -> Tuple[Iterable[Any], ...]

def limits(items: Iterable[Any]) -> Tuple[Any, Any]:
    """A possible way to get limits from an iterable.
    This has unpleasant consequences on the original iterable, though,
    since this functions consumes it.

    >>> data = iter( [1,9,2,8,3,7,4,6,5] )
    >>> limits(data)
    (9, 1)
    >>> list(data)
    []
    """
    max_tee, min_tee = itertools.tee(items, 2)
    return max(max_tee), min(min_tee)

from collections import Sequence
def mean(items: Sequence) -> float:
    return sum(items)/len(items)

test_parse_1 = """
>>> with urllib.request.urlopen("file:./Winter%202012-2013.kml") as source:
...     v0= list(row_iter_kml(source))
>>> len(v0)
74
>>> v0[0]
['-76.33029518659048', '37.54901619777347', '0']
>>> v0[-1]
['-76.47350299999999', '38.976334', '0']

>>> with urllib.request.urlopen("file:./Winter%202012-2013.kml") as source:
...     v1= tuple(float_lat_lon_a(row_iter_kml(source)))
>>> len(v1)
74
>>> v1[0]
('37.54901619777347', '-76.33029518659048')
>>> v1[-1]
('38.976334', '-76.47350299999999')

>>> with urllib.request.urlopen("file:./Winter%202012-2013.kml") as source:
...     v2= tuple(float_lat_lon(row_iter_kml(source)))
>>> len(v2)
74
>>> v2[0]
(37.54901619777347, -76.33029518659048)
>>> v2[-1]
(38.976334, -76.473503)

>>> with urllib.request.urlopen("file:./Winter%202012-2013.kml") as source:
...     trip = list(
...         legs(
...            (float(lat), float(lon)) 
...            for lat,lon in lat_lon_kml(row_iter_kml(source))
...         )
...     )
...
>>> trip  # doctest: +ELLIPSIS
[((37.54901619777347, -76.33029518659048), (37.840832, -76.273834)), ..., ((38.330166, -76.458504), (38.976334, -76.473503))]
"""

test_parse_2 = """
>>> with urllib.request.urlopen("file:./Winter%202012-2013.kml") as source:
...     v0= tuple(legs(float_lat_lon(row_iter_kml(source)) ) )
>>> len(v0)
73
>>> v0[0]
((37.54901619777347, -76.33029518659048), (37.840832, -76.273834))
>>> v0[-1]
((38.330166, -76.458504), (38.976334, -76.473503))

>>> with urllib.request.urlopen("file:./Winter%202012-2013.kml") as source:
...     v1= tuple(pairs(float_lat_lon(row_iter_kml(source)) ) )
>>> len(v1)
73
>>> v1[0]
((37.54901619777347, -76.33029518659048), (37.840832, -76.273834))
>>> v1[-1]
((38.330166, -76.458504), (38.976334, -76.473503))

>>> with urllib.request.urlopen("file:./Winter%202012-2013.kml") as source:
...     v2= tuple(legs( float_from_pair(lat_lon_kml(row_iter_kml(source)))))
>>> len(v2)
73
>>> v2[0]
((37.54901619777347, -76.33029518659048), (37.840832, -76.273834))
>>> v2[-1]
((38.330166, -76.458504), (38.976334, -76.473503))

"""

test_parse_3 = """
>>> with urllib.request.urlopen("file:./Winter%202012-2013.kml") as source:
...     flt= tuple( (float(lat), float(lon)) for lat,lon in float_lat_lon(row_iter_kml(source)) )
>>> len(flt)
74
>>> flt[0]
(37.54901619777347, -76.33029518659048)
>>> flt[-1]
(38.976334, -76.473503)

"""

test_haversine = """
>>> trip = iter([ (0,0), (1,0), (1,1), (0,1), (0,0) ]) # about 240 NM

>>> [ (lat, lon, round(haversine(lat, lon),4)) for lat,lon in legs(trip) ]
[((0, 0), (1, 0), 60.0393), ((1, 0), (1, 1), 60.0302), ((1, 1), (0, 1), 60.0393), ((0, 1), (0, 0), 60.0393)]
"""


__test__ = {
    'basic parse': test_parse_1,
    'pairs of legs': test_parse_2,
    'another basic parse': test_parse_3,
    'haversine': test_haversine,
}


def test():
    import doctest
    doctest.testmod(verbose=True)

if __name__ == "__main__":
    test()
