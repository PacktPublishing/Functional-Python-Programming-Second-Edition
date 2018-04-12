#!/usr/bin/env python3
"""Functional Python Programming

Chapter 5, Example Set 2
"""
import dis
from typing import Callable, Iterable, Iterator

def mapping1(f: Callable, C: Iterable) -> Iterator:
    """
    >>> list(mapping1( lambda x: 2**x, range(32) ))
    [1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096, 8192, 16384, 32768, 65536, 131072, 262144, 524288, 1048576, 2097152, 4194304, 8388608, 16777216, 33554432, 67108864, 134217728, 268435456, 536870912, 1073741824, 2147483648]
    """
    return (f(a) for a in C)

def mapping2(f: Callable, C: Iterable) -> Iterator:
    """
    >>> list(mapping2( lambda x: 2**x, range(32) ))
    [1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096, 8192, 16384, 32768, 65536, 131072, 262144, 524288, 1048576, 2097152, 4194304, 8388608, 16777216, 33554432, 67108864, 134217728, 268435456, 536870912, 1073741824, 2147483648]
    """
    for a in C:
        yield f(a)

def performance():
    print("Generator Expression")
    dis.dis(mapping1)
    print(
        timeit.timeit(
            """list(mapping1( lambda x: 2**x, range(32) ))""",
            """
def mapping1( f, C ):
    return (f(a) for a in C)
            """
            )
        )

    print("Generator Function")
    dis.dis(mapping2)
    print(
        timeit.timeit(
            """list(mapping2( lambda x: 2**x, range(32) ))""",
            """
def mapping2( f, C ):
    for a in C:
       yield f(a)
            """
            )
        )

def test():
    import doctest
    doctest.testmod(verbose=1)

if __name__ == "__main__":
    #import timeit
    #performace()
    test()
