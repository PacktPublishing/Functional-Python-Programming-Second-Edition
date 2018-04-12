#!/usr/bin/env python3
"""Functional Python Programming

Chapter 5, Example Set 3
"""
# pylint: disable=wrong-import-position,reimported

import math
from typing import Callable
from typing import Optional, Any

class NullAware:
    def __init__(self, some_func: Callable[[Any], Any]) -> None:
        self.some_func = some_func
    def __call__(self, arg: Optional[Any]) -> Optional[Any]:
        return None if arg is None else self.some_func(arg)

null_log_scale = NullAware(math.log)
null_round_4 = NullAware(lambda x: round(x, 4))

test_NullAware = """
>>> some_data = [ 10, 100, None, 50, 60 ]
>>> scaled = map( null_log_scale, some_data )
>>> [null_round_4(v) for v in scaled]
[2.3026, 4.6052, None, 3.912, 4.0943]
"""

from typing import Callable, Iterable
class Sum_Filter:
    __slots__ = ["filter", "function"]
    def __init__(self,
                 filter_f: Callable[[Any], bool],
                 func: Callable[[Any], float]) -> None:
        self.filter = filter_f
        self.function = func
    def __call__(self, iterable: Iterable) -> float:
        return sum(self.function(x) for x in iterable if self.filter(x))

count_not_none = Sum_Filter(lambda x: x is not None, lambda x: 1)

test_Sum_Filter = """
>>> some_data = [10, 100, None, 50, 60]
>>> count_not_none(some_data)
4
"""


__test__ = {
    "test_NullAware": test_NullAware,
    "test_Sum_Filter": test_Sum_Filter,
}

def test():
    import doctest
    doctest.testmod(verbose=1)

if __name__ == "__main__":
    #performace()
    test()
