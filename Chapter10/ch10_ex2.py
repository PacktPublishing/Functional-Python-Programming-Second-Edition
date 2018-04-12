#!/usr/bin/env python3
"""Functional Python Programming

Chapter 10, Example Set 2
"""
# pylint: disable=wrong-import-position

from numbers import Number
from functools import total_ordering
from typing import NamedTuple

class Card1(NamedTuple):
    rank: int
    suit: str

test_card1 = """
>>> c2s= Card1(2, '\u2660')
>>> c2s.rank
2
>>> c2s.suit
'\u2660'
>>> c2s
Card1(rank=2, suit='♠')
>>> len(c2s)
2

This is *incorrect* behavior for games where
rank is the only relevant attribute

>>> c2h= Card1(2, '\u2665')
>>> c2h == c2s
False
>>> "{0}== {1}: {2}".format( c2s, c2h, c2h == c2s )
"Card1(rank=2, suit='♠')== Card1(rank=2, suit='♥'): False"
"""

from typing import Union, Any
CardInt = Union['Card', int]

@total_ordering
class Card(tuple):
    """Immutable object; rank-only comparisons.
    
    Old School. 

    Suits= '\u2660', '\u2665', '\u2666', '\u2663'
    """
    __slots__ = ()
    def __new__(cls, rank, suit):
        obj = super().__new__(Card, (suit, rank))
        return obj
    def __repr__(self) -> str:
        return "{0.rank}{0.suit}".format(self)
    @property
    def rank(self) -> int:
        return self[1]
    @property
    def suit(self) -> str:
        return self[0]
    def __eq__(self, other: Any) -> bool:
        if isinstance(other, Card):
            return self.rank == other.rank
        elif isinstance(other, int):
            return self.rank == other
        return NotImplemented
    def __lt__(self, other: Any) -> bool:
        if isinstance(other, Card):
            return self.rank < other.rank
        elif isinstance(other, int):
            return self.rank < other
        return NotImplemented

test_eq = """
>>> c2s= Card(2, '\u2660')
>>> c2s.rank
2
>>> c2s.suit
'\u2660'
>>> c2s
2\u2660
>>> len(c2s)
2

This is correct behavior for games where
rank is the only relevant attribute

>>> c2h= Card(2, '\u2665')
>>> c2h == c2s
True
>>> "{0}== {1}: {2}".format(c2s, c2h, c2h == c2s)
'2\u2660== 2\u2665: True'
>>> c2h == 2
True
>>> 2 == c2h
True
"""

test_order = """
>>> c2s= Card(2, '\u2660')
>>> c3h= Card(3, '\u2665')
>>> c4c= Card(4, '\u2663')
>>> c2s <= c3h < c4c
True
>>> c3h >= c3h
True
>>> c3h > c2s
True
>>> c4c != c2s
True
"""

extra_comparisons = """
These don't work, the logic doesn't fit with total_ordering.

>>> c4c= Card(4, '\u2663')
>>> try:
...     print("c4c > 3", c4c > 3)
... except TypeError as e:
...     print(e)
'>' not supported between instances of 'Card' and 'int'
>>> try:
...     print("3 < c4c", 3 < c4c)
... except TypeError as e:
...     print(e)
'<' not supported between instances of 'int' and 'Card'
"""

@total_ordering
class Card2(NamedTuple):
    rank: int
    suit: str
    def __str__(self) -> str:
        return "{0.rank}{0.suit}".format(self)
    def __eq__(self, other: Any) -> bool:
        if isinstance(other, Card2):
            return self.rank == other.rank
        elif isinstance(other, int):
            return self.rank == other
        return NotImplemented
    def __lt__(self, other: Any) -> bool:
        if isinstance(other, Card2):
            return self.rank < other.rank
        elif isinstance(other, int):
            return self.rank < other
        return NotImplemented
    
test_eq_2 = """
>>> c2s = Card2(2, '\u2660')
>>> c2s.rank
2
>>> c2s.suit
'\u2660'
>>> c2s
Card2(rank=2, suit='\u2660')
>>> len(c2s)
2

This is correct behavior for games where
rank is the only relevant attribute

>>> c2h= Card2(2, '\u2665')
>>> c2h == c2s
True
>>> "{0} == {1}: {2}".format(c2s, c2h, c2h == c2s)
'2\u2660 == 2\u2665: True'
>>> c2h == 2
True
>>> 2 == c2h
True
"""

test_order_2 = """
>>> c2s= Card2(2, '\u2660')
>>> c3h= Card2(3, '\u2665')
>>> c4c= Card2(4, '\u2663')
>>> c2s <= c3h < c4c
True
>>> c3h >= c3h
True
>>> c3h > c2s
True
>>> c4c != c2s
True
"""

extra_comparisons_2 = """
These don't work, the logic doesn't fit with total_ordering.

>>> c4c= Card2(4, '\u2663')
>>> try:
...     print("c4c > 3", c4c > 3)
... except TypeError as e:
...     print(e)
'>' not supported between instances of 'Card2' and 'int'
>>> try:
...     print("3 < c4c", 3 < c4c)
... except TypeError as e:
...     print(e)
'<' not supported between instances of 'int' and 'Card2'
"""

__test__ = {
    "test_card1": test_card1,
    "test_eq": test_eq,
    "test_order": test_order,
    "extra_comparisons": extra_comparisons,
    "test_eq_2": test_eq_2,
    "test_order_2": test_order_2,
    "extra_comparisons_2": extra_comparisons_2,
    }

def test():
    import doctest
    doctest.testmod(verbose=1)

if __name__ == "__main__":
    test()
