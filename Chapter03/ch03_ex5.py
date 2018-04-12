#!/usr/bin/env python3
"""Functional Python Programming

Chapter 3, Example Set 5
"""
# pylint: disable=line-too-long,wrong-import-position

import csv
from typing import TextIO, Iterator, List, Text, Iterable

def row_iter(source: TextIO) -> Iterator[List[Text]]:
    """Read a CSV file and emit a sequence of rows.

    >>> import io
    >>> data= io.StringIO( "1\\t2\\t3\\n4\\t5\\t6\\n" )
    >>> list(row_iter(data))
    [['1', '2', '3'], ['4', '5', '6']]
    """
    rdr = csv.reader(source, delimiter="\t")
    return rdr

from typing import Optional
def float_none(data: Text) -> Optional[float]:
    """Float conversion: return None instead of ValueError exception.

    >>> float_none('abc')
    >>> float_none('1.23')
    1.23
    """
    try:
        data_f = float(data)
        return data_f
    except ValueError:
        return None

from typing import Callable, List, Optional
def head_map_filter(row_iter: Iterator[List[Optional[Text]]]) -> Iterator[List[float]]:
    """Removing headers by applying a filter to get rows with 8 values.

    >>> rows= [ ["Anscombe's quartet"], ['I', 'II', 'III', 'IV'], ['x','y','x','y','x','y','x','y'], ['1','2','3','4','5','6','7','8']]
    >>> list(head_map_filter( rows ))
    [[1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0]]
    """
    R_Text = List[Optional[Text]]
    R_Float = List[Optional[float]]

    float_row: Callable[[R_Text], R_Float] \
        = lambda row: list(map(float_none, row))

    all_numeric: Callable[[R_Float], bool] \
        = lambda row: all(row) and len(row) == 8

    return filter(all_numeric, map(float_row, row_iter))

def head_split_fixed(row_iter: Iterator[List[Text]]) -> Iterator[List[Text]]:
    """Removing a fixed sequence of headers.

    >>> rows= [ ["Anscombe's quartet"], ['I', 'II', 'III', 'IV'], ['x','y','x','y','x','y','x','y'], ['1','2','3','4','5','6','7','8']]
    >>> list(head_split_fixed( iter(rows) ))
    [['1', '2', '3', '4', '5', '6', '7', '8']]
    """
    title = next(row_iter)
    assert (len(title) == 1
            and title[0] == "Anscombe's quartet")
    heading = next(row_iter)
    assert (len(heading) == 4
            and heading == ['I', 'II', 'III', 'IV'])
    columns = next(row_iter)
    assert (len(columns) == 8
            and columns == ['x', 'y', 'x', 'y', 'x', 'y', 'x', 'y'])
    return row_iter

def head_split_recurse(row_iter: Iterator[List[Text]]) -> Iterator[List[Text]]:
    """Removing headers recusively, looking for the last header.

    >>> rows= [ ["Anscombe's quartet"], ['I', 'II', 'III', 'IV'], ['x','y','x','y','x','y','x','y'], ['1','2','3','4','5','6','7','8']]
    >>> list(head_split_recurse( iter(rows) ))
    [['1', '2', '3', '4', '5', '6', '7', '8']]
    """
    data = next(row_iter)
    if len(data) == 8 and data == ['x', 'y', 'x', 'y', 'x', 'y', 'x', 'y']:
        return row_iter
    return head_split_recurse(row_iter)

from typing import Tuple, cast, TypeVar

T_ = TypeVar("T_")
Pair = Tuple[T_, T_]
def series(n: int, row_iter: Iterable[List[T_]]) -> Iterator[Pair]:
    """Turn one of the given Anscombe's series into two-tuple objects.

    >>> rows = [[1,2, 3,4, 5,6, 7,8],[9,10, 11,12, 13,14, 15,16]]
    >>> list(series(0, rows))
    [(1, 2), (9, 10)]
    >>> list(series(1, rows))
    [(3, 4), (11, 12)]
    """
    for row in row_iter:
        yield cast(Pair, tuple(row[n*2:n*2+2]))

from typing import Callable, Iterable
row_float: Callable[[Pair], Iterable[float]] = lambda row: map(float, row)

test_parse_1 = """
>>> with open("Anscombe.txt") as source:
...     print(list(head_map_filter(row_iter(source))))
[[10.0, 8.04, 10.0, 9.14, 10.0, 7.46, 8.0, 6.58], [8.0, 6.95, 8.0, 8.14, 8.0, 6.77, 8.0, 5.76], [13.0, 7.58, 13.0, 8.74, 13.0, 12.74, 8.0, 7.71], [9.0, 8.81, 9.0, 8.77, 9.0, 7.11, 8.0, 8.84], [11.0, 8.33, 11.0, 9.26, 11.0, 7.81, 8.0, 8.47], [14.0, 9.96, 14.0, 8.1, 14.0, 8.84, 8.0, 7.04], [6.0, 7.24, 6.0, 6.13, 6.0, 6.08, 8.0, 5.25], [4.0, 4.26, 4.0, 3.1, 4.0, 5.39, 19.0, 12.5], [12.0, 10.84, 12.0, 9.13, 12.0, 8.15, 8.0, 5.56], [7.0, 4.82, 7.0, 7.26, 7.0, 6.42, 8.0, 7.91], [5.0, 5.68, 5.0, 4.74, 5.0, 5.73, 8.0, 6.89]]

>>> with open("Anscombe.txt") as source:
...     print(list(head_split_fixed(row_iter(source))))
[['10.0', '8.04', '10.0', '9.14', '10.0', '7.46', '8.0', '6.58'], ['8.0', '6.95', '8.0', '8.14', '8.0', '6.77', '8.0', '5.76'], ['13.0', '7.58', '13.0', '8.74', '13.0', '12.74', '8.0', '7.71'], ['9.0', '8.81', '9.0', '8.77', '9.0', '7.11', '8.0', '8.84'], ['11.0', '8.33', '11.0', '9.26', '11.0', '7.81', '8.0', '8.47'], ['14.0', '9.96', '14.0', '8.10', '14.0', '8.84', '8.0', '7.04'], ['6.0', '7.24', '6.0', '6.13', '6.0', '6.08', '8.0', '5.25'], ['4.0', '4.26', '4.0', '3.10', '4.0', '5.39', '19.0', '12.50'], ['12.0', '10.84', '12.0', '9.13', '12.0', '8.15', '8.0', '5.56'], ['7.0', '4.82', '7.0', '7.26', '7.0', '6.42', '8.0', '7.91'], ['5.0', '5.68', '5.0', '4.74', '5.0', '5.73', '8.0', '6.89']]

>>> with open("Anscombe.txt") as source:
...     print(list(head_split_recurse(row_iter(source))))
[['10.0', '8.04', '10.0', '9.14', '10.0', '7.46', '8.0', '6.58'], ['8.0', '6.95', '8.0', '8.14', '8.0', '6.77', '8.0', '5.76'], ['13.0', '7.58', '13.0', '8.74', '13.0', '12.74', '8.0', '7.71'], ['9.0', '8.81', '9.0', '8.77', '9.0', '7.11', '8.0', '8.84'], ['11.0', '8.33', '11.0', '9.26', '11.0', '7.81', '8.0', '8.47'], ['14.0', '9.96', '14.0', '8.10', '14.0', '8.84', '8.0', '7.04'], ['6.0', '7.24', '6.0', '6.13', '6.0', '6.08', '8.0', '5.25'], ['4.0', '4.26', '4.0', '3.10', '4.0', '5.39', '19.0', '12.50'], ['12.0', '10.84', '12.0', '9.13', '12.0', '8.15', '8.0', '5.56'], ['7.0', '4.82', '7.0', '7.26', '7.0', '6.42', '8.0', '7.91'], ['5.0', '5.68', '5.0', '4.74', '5.0', '5.73', '8.0', '6.89']]

"""

test_parse_2 = """
>>> with open("Anscombe.txt") as source:
...     print( list(series(0, head_split_recurse(row_iter(source)))) )
[('10.0', '8.04'), ('8.0', '6.95'), ('13.0', '7.58'), ('9.0', '8.81'), ('11.0', '8.33'), ('14.0', '9.96'), ('6.0', '7.24'), ('4.0', '4.26'), ('12.0', '10.84'), ('7.0', '4.82'), ('5.0', '5.68')]

>>> with open("Anscombe.txt") as source:
...     print( list(series(0, head_map_filter(row_iter(source)))) )
[(10.0, 8.04), (8.0, 6.95), (13.0, 7.58), (9.0, 8.81), (11.0, 8.33), (14.0, 9.96), (6.0, 7.24), (4.0, 4.26), (12.0, 10.84), (7.0, 4.82), (5.0, 5.68)]

>>> with open("Anscombe.txt") as source:
...     data = head_split_fixed(row_iter(source))
...     print( list(series(0,data)) )
[('10.0', '8.04'), ('8.0', '6.95'), ('13.0', '7.58'), ('9.0', '8.81'), ('11.0', '8.33'), ('14.0', '9.96'), ('6.0', '7.24'), ('4.0', '4.26'), ('12.0', '10.84'), ('7.0', '4.82'), ('5.0', '5.68')]

>>> with open("Anscombe.txt") as source:
...     data = head_split_fixed(row_iter(source))
...     sample_I= tuple(series(0,data))
...     print( sample_I )
(('10.0', '8.04'), ('8.0', '6.95'), ('13.0', '7.58'), ('9.0', '8.81'), ('11.0', '8.33'), ('14.0', '9.96'), ('6.0', '7.24'), ('4.0', '4.26'), ('12.0', '10.84'), ('7.0', '4.82'), ('5.0', '5.68'))

"""

test_mean = """
>>> with open("Anscombe.txt") as source:
...     data = tuple(head_split_fixed(row_iter(source)))
...     sample_I = tuple(series(0,data))
...     sample_II = tuple(series(1,data))
...     sample_III = tuple(series(2,data))
...     sample_IV = tuple(series(3,data))

>>> for subset in sample_I, sample_II, sample_III, sample_III:
...     mean = sum(float(pair[1]) for pair in subset)/len(subset)
...     print( round(mean,3) )
7.501
7.501
7.5
7.5
"""

__test__ = {
    "Basic Parse": test_parse_1,
    "Pick Series": test_parse_2,
    "Basic Mean": test_mean,
}

def test():
    import doctest
    doctest.testmod(verbose=1)

if __name__ == "__main__":
    test()
