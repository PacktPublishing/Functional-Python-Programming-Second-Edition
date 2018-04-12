#!/usr/bin/env python3
"""Functional Python Programming

Chapter 14, Example Set 2
"""
# pylint: disable=wrong-import-order

from pymonad import curry, Just, List

@curry
def read_header(file):
    _ = file.readline()
    _ = file.readline()
    _ = file.readline()
    return Just([])

@curry
def read_rest(file, data):
    # file, data = file_data[0], file_data[1]
    txt = file.readline().rstrip()
    if txt:
        row = float * List(*txt.split("\t"))
        return Just(data + [list(row)]) >> read_rest(file)
    return Just(data)

def anscombe():
    """
    >>> d= anscombe()
    >>> d[0]
    [10.0, 8.04, 10.0, 9.14, 10.0, 7.46, 8.0, 6.58]
    >>> d[-1]
    [5.0, 5.68, 5.0, 4.74, 5.0, 5.73, 8.0, 6.89]
    """
    with open("Anscombe.txt") as source:
        data = Just([]) >> read_header(source) >> read_rest(source)
        data = data.getValue()
        return data

import random

def rng():
    return (random.randint(1, 6), random.randint(1, 6))

@curry
def come_out_roll(dice, status):
    d = dice()
    if sum(d) in (7, 11):
        return Just(("win", sum(d), [d]))
    elif sum(d) in (2, 3, 12):
        return Just(("lose", sum(d), [d]))
    return Just(("point", sum(d), [d]))

@curry
def point_roll(dice, status):
    prev, point, so_far = status
    if prev != "point":
        return Just(status)
    d = dice()
    if sum(d) == 7:
        return Just(("craps", point, so_far+[d]))
    elif sum(d) == point:
        return Just(("win", point, so_far+[d]))
    return Just(("point", point, so_far+[d])) >> point_roll(dice)

def craps(dice):
    """
    >>> def seven():
    ...    return (3,4)
    >>> craps( seven )
    ('win', 7, [(3, 4)])
    >>> rolls= [(3,3), (2,2), (3,3)]
    >>> def fixed():
    ...    global rolls
    ...    head, *tail = rolls
    ...    rolls= tail
    ...    return head
    >>> craps( fixed )
    ('win', 6, [(3, 3), (2, 2), (3, 3)])
    """
    outcome = (
        Just(("", 0, [])) >> come_out_roll(dice)
        >> point_roll(dice)
    )
    print(outcome.getValue())

def test():
    import doctest
    doctest.testmod(verbose=1)

def demo():
    """
    Play 10 rounds of craps.
    """
    for _ in range(10):
        craps(rng)

if __name__ == "__main__":
    test()
    demo()
