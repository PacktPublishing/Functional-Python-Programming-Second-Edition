#!/usr/bin/env python3
"""Functional Python Programming

Chapter 10, Example Set 4
"""
# pylint: disable=wrong-import-position

from functools import reduce, partial

display = lambda data: reduce(lambda x, y: print(x, y), data)
sum2 = lambda data: reduce(lambda x, y: x+y**2, data, 0)
sum = lambda data: reduce(lambda x, y: x+y, data, 0)
count = lambda data: reduce(lambda x, y: x+1, data, 0)
min = lambda data: reduce(lambda x, y: x if x < y else y, data)
max = lambda data: reduce(lambda x, y: x if x > y else y, data)

test_reductions = """
>>> import math
>>> d = [ 2, 4, 4, 4, 5, 5, 7, 9 ]
>>> sum2(d)
232
>>> sum(d)
40
>>> count(d)
8
>>> sum(d)/count(d)
5.0
>>> math.sqrt((sum2(d)/count(d))-(sum(d)/count(d))**2)
2.0
>>> max(d)
9
>>> min(d)
2
"""

from typing import Callable, Iterable, TypeVar
T_ = TypeVar("T_")
def map_reduce(
        map_fun: Callable[[T_], T_],
        reduce_fun: Callable[[T_, T_], T_],
        source: Iterable[T_]) -> T_:
    """
    This example doesn't *actually* fit the type definitions!
    
    This involves a mapping transformation from T1_ to T2_,
    Then the reduce works with T2_.
    
    Either we have to provide super-complex type definitions,
    or resort to using ``Any``. 
    
    >>> from operator import add
    >>> data = ["2", "3", "5", "7"]
    >>> map_reduce(int, add, data)
    17
    """
    return reduce(reduce_fun, map(map_fun, source))

def sum2_mr(source: Iterable[float]) -> float:
    """
    >>> d = [2, 4, 4, 4, 5, 5, 7, 9]
    >>> sum2_mr(d)
    232
    """
    return map_reduce(lambda y: y**2, lambda x, y: x+y, source)

import operator
def sum2_mr2(source: Iterable[float]) -> float:
    """
    >>> d = [2, 4, 4, 4, 5, 5, 7, 9]
    >>> sum2_mr2(d)
    232
    """
    return map_reduce(lambda y: y**2, operator.add, source)

def count_mr(source: Iterable[float]) -> float:
    """
    >>> d = [2, 4, 4, 4, 5, 5, 7, 9]
    >>> count_mr(d)
    8
    """
    return map_reduce(lambda y: 1, lambda x, y: x+y, source)

def comma_fix(data: str) -> float:
    try:
        return float(data)
    except ValueError:
        return float(data.replace(",", ""))

def clean_sum(
        cleaner: Callable[[str], float],
        data: Iterable[str]
    ) -> float:
    """
    >>> d = ('1,196', '1,176', '1,269', '1,240', '1,307',
    ... '1,435', '1,601', '1,654', '1,803', '1,734')
    >>> clean_sum(comma_fix, d)
    14415.0
    """
    return reduce(operator.add, map(cleaner, data))

sum_p = partial(reduce, operator.add)

test_sump = """
>>> iterable = [2, 4, 4, 4, 5, 5, 7, 9]
>>> sum_p(iterable)
40
>>> sum_p(map(lambda x:x**2, iterable))
232
>>> reduce(lambda x, y: x+y**2, iterable, 0)
232
>>> reduce(lambda x, y: x+y**2, iterable)
230
"""

def performance():
    import timeit
    import sys
    for source_len in range(100, 1000, 100):
        data = repr(['x']*source_len)
        op_r = f'reduce( operator.add, {data}, "" )'
        op_j = f'"".join({data})'
        r = timeit.timeit(
            op_r,
            """from functools import reduce; import operator""")
        j = timeit.timeit(
            op_j)
        print('reduce', source_len, r)
        print('join', source_len, j)
        sys.stdout.flush()

__test__ = {
    "test_reductions": test_reductions,
    "test_sump": test_sump,
}

def test():
    import doctest
    doctest.testmod(verbose=1)

if __name__ == "__main__":
    test()
    # performance()
