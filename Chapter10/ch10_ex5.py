#!/usr/bin/env python3
"""Functional Python Programming

Chapter 10, Example Set 5
"""

from collections import defaultdict
from typing import (
    Iterable, Callable, Dict, List, TypeVar,
    Iterator, Tuple, cast)
D_ = TypeVar("D_")
K_ = TypeVar("K_")
def partition(
        source: Iterable[D_],
        key: Callable[[D_], K_] = lambda x: cast(K_, x)
    ) -> Iterable[Tuple[K_, Iterator[D_]]]:
    """Sort not required."""
    pd: Dict[K_, List[D_]] = defaultdict(list)
    for item in source:
        pd[key(item)].append(item)
    for k in sorted(pd):
        yield k, iter(pd[k])

from itertools import groupby

def partition_s(
        source: Iterable[D_],
        key: Callable[[D_], K_] = lambda x: cast(K_, x)
    ) -> Iterable[Tuple[K_, Iterator[D_]]]:
    """Sort required"""
    return groupby(sorted(source, key=key), key)


test_data = """
>>> data = [('4', 6.1), ('1', 4.0), ('2', 8.3), ('2', 6.5),
... ('1', 4.6), ('2', 6.8), ('3', 9.3), ('2', 7.8),
... ('2', 9.2), ('4', 5.6), ('3', 10.5), ('1', 5.8),
... ('4', 3.8), ('3', 8.1), ('3', 8.0), ('1', 6.9),
... ('3', 6.9), ('4', 6.2), ('1', 5.4), ('4', 5.8)]

>>> for key, group_iter in partition(data, key=lambda x:x[0]):
...     print(key, tuple(group_iter))
1 (('1', 4.0), ('1', 4.6), ('1', 5.8), ('1', 6.9), ('1', 5.4))
2 (('2', 8.3), ('2', 6.5), ('2', 6.8), ('2', 7.8), ('2', 9.2))
3 (('3', 9.3), ('3', 10.5), ('3', 8.1), ('3', 8.0), ('3', 6.9))
4 (('4', 6.1), ('4', 5.6), ('4', 3.8), ('4', 6.2), ('4', 5.8))
>>> for key, group_iter in partition_s(data, key=lambda x:x[0]):
...     print(key, tuple(group_iter))
1 (('1', 4.0), ('1', 4.6), ('1', 5.8), ('1', 6.9), ('1', 5.4))
2 (('2', 8.3), ('2', 6.5), ('2', 6.8), ('2', 7.8), ('2', 9.2))
3 (('3', 9.3), ('3', 10.5), ('3', 8.1), ('3', 8.0), ('3', 6.9))
4 (('4', 6.1), ('4', 5.6), ('4', 3.8), ('4', 6.2), ('4', 5.8))

"""

mean = lambda seq: sum(seq)/len(seq)
var = lambda mean, seq: sum((x-mean)**2/mean for x in seq)

Item = Tuple[K_, float]
def summarize(
        key_iter: Tuple[K_, Iterable[Item]]
    ) -> Tuple[K_, float, float]:
    key, item_iter = key_iter
    values = tuple(v for k, v in item_iter)
    m = mean(values)
    return key, m, var(m, values)

test_summarize = """
>>> data = [('4', 6.1), ('1', 4.0), ('2', 8.3), ('2', 6.5), ('1', 4.6),
... ('2', 6.8), ('3', 9.3), ('2', 7.8), ('2', 9.2), ('4', 5.6),
... ('3', 10.5), ('1', 5.8), ('4', 3.8), ('3', 8.1), ('3', 8.0),
... ('1', 6.9), ('3', 6.9), ('4', 6.2), ('1', 5.4), ('4', 5.8)]

>>> partition1= partition( data, key=lambda x:x[0] )
>>> groups1= map( summarize, partition1 )
>>> for g, s, s2 in groups1:
...     print( g, round(s,2), round(s2,2) )
1 5.34 0.93
2 7.72 0.63
3 8.56 0.89
4 5.5 0.7

>>> partition2= partition_s( data, key=lambda x:x[0] )
>>> groups2= map( summarize, partition2 )
>>> for g, s, s2 in groups2:
...     print( g, round(s,2), round(s2,2) )
1 5.34 0.93
2 7.72 0.63
3 8.56 0.89
4 5.5 0.7


"""

__test__ = {
    "test_data": test_data,
    "test_summarize": test_summarize,
}

def test():
    import doctest
    doctest.testmod(verbose=1)

if __name__ == "__main__":
    test()
    #performance()
