#!/usr/bin/env python3
"""Functional Python Programming

Chapter 7, Example Set 4
"""
# pylint: disable=wrong-import-position,reimported

# Even more generic Rank-Order processing.

# from collections import namedtuple
# Rank_Data = namedtuple("Rank_Data", ("rank_seq", "raw"))

from typing import NamedTuple, Tuple, Any
class Rank_Data(NamedTuple):
    """
    Two similar variations:
    - Rank_Data((rank,), data) -- singleton ranking
    - Rank_Data((rank, rank), data)
    
    >>> data = {'key1': 1, 'key2': 2}
    >>> r = Rank_Data((2, 7), data)
    >>> r.rank_seq[0]
    2
    >>> r.raw
    {'key1': 1, 'key2': 2}
    """
    rank_seq: Tuple[float]
    raw: Any

from typing import (
    Callable, Sequence, Iterator, Union, Iterable, TypeVar, cast,
    Union
)
K_ = TypeVar("K_")  # Some comparable key type used for ranking.
Source = Union[Rank_Data, Any]  # Generic with respect to the source
def rank_data(
        seq_or_iter: Union[Sequence[Source], Iterator[Source]],
        key: Callable[[Rank_Data], K_] = lambda obj: cast(K_, obj)
    ) -> Iterable[Rank_Data]:
    """Rank raw data by creating Rank_Data objects from an iterable.
    Or rerank existing data by creating new Rank_Data objects from
    old Rank_Data objects.

    >>> scalars = [0.8, 1.2, 1.2, 2.3, 18]
    >>> list(rank_data(scalars))  # doctest: +NORMALIZE_WHITESPACE
    [Rank_Data(rank_seq=(1.0,), raw=0.8), Rank_Data(rank_seq=(2.5,), raw=1.2),
     Rank_Data(rank_seq=(2.5,), raw=1.2), Rank_Data(rank_seq=(4.0,), raw=2.3),
     Rank_Data(rank_seq=(5.0,), raw=18)]

    >>> pairs = ((2, 0.8), (3, 1.2), (5, 1.2), (7, 2.3), (11, 18))
    >>> rank_x = tuple(rank_data(pairs, key=lambda x:x[0] ))
    >>> rank_x  # doctest: +NORMALIZE_WHITESPACE
    (Rank_Data(rank_seq=(1.0,), raw=(2, 0.8)),
     Rank_Data(rank_seq=(2.0,), raw=(3, 1.2)),
     Rank_Data(rank_seq=(3.0,), raw=(5, 1.2)),
     Rank_Data(rank_seq=(4.0,), raw=(7, 2.3)),
     Rank_Data(rank_seq=(5.0,), raw=(11, 18)))
    >>> rank_xy = (rank_data(rank_x, key=lambda x:x[1] ))
    >>> tuple(rank_xy)  # doctest: +NORMALIZE_WHITESPACE
    (Rank_Data(rank_seq=(1.0, 1.0), raw=(2, 0.8)),
     Rank_Data(rank_seq=(2.0, 2.5), raw=(3, 1.2)),
     Rank_Data(rank_seq=(3.0, 2.5), raw=(5, 1.2)),
     Rank_Data(rank_seq=(4.0, 4.0), raw=(7, 2.3)),
     Rank_Data(rank_seq=(5.0, 5.0), raw=(11, 18)))
    """
    if isinstance(seq_or_iter, Iterator):
        # Not a sequence? Materialize a sequence object.
        yield from rank_data(list(seq_or_iter), key)
        return
    data: Sequence[Rank_Data]
    if isinstance(seq_or_iter[0], Rank_Data):
        # Collection of Rank_Data is what we prefer.
        data = seq_or_iter
    else:
        # Collection of non-Rank_Data? Convert to Rank_Data and process.
        empty_ranks: Tuple[float] = cast(Tuple[float], ())
        data = list(
            Rank_Data(empty_ranks, raw_data)
            for raw_data in cast(Sequence[Source], seq_or_iter)
        )

    for r, rd in rerank(data, key):
        new_ranks = cast(Tuple[float], rd.rank_seq + cast(Tuple[float], (r,)))
        yield Rank_Data(new_ranks, rd.raw)

from typing import Callable, Tuple, Iterator, Iterable, TypeVar, cast
def rerank(
        rank_data_iter: Iterable[Rank_Data],
        key: Callable[[Rank_Data], K_]
    ) -> Iterator[Tuple[float, Rank_Data]]:
    """Re-rank by adding another rank order to a Rank_Data object.
    """
    sorted_iter = iter(
        sorted(
            rank_data_iter, key=lambda obj: key(obj.raw)
        )
    )
    # Apply ranker to `head, *tail = sorted(rank_data_iter)`
    head = next(sorted_iter)
    yield from ranker(sorted_iter, 0, [head], key)

from typing import Iterator, Tuple
def yield_sequence(
        rank: float,
        same_rank_iter: Iterator[Rank_Data]
    ) -> Iterator[Tuple[float, Rank_Data]]:
    """Emit a sequence of same rank values."""
    head = next(same_rank_iter)
    yield rank, head
    yield from yield_sequence(rank, same_rank_iter)

from typing import List
def ranker(
        sorted_iter: Iterator[Rank_Data],
        base: float,
        same_rank_seq: List[Rank_Data],
        key: Callable[[Rank_Data], K_]
    ) -> Iterator[Tuple[float, Rank_Data]]:
    """Rank values from a sorted_iter using a base rank value.
    If the next value's key matches same_rank_seq, accumulate those.
    If the next value's key is different, accumulate same rank values
    and start accumulating a new sequence.

    >>> scalars= [0.8, 1.2, 1.2, 2.3, 18]
    >>> list(rank_data(scalars))  # doctest: +NORMALIZE_WHITESPACE
    [Rank_Data(rank_seq=(1.0,), raw=0.8), Rank_Data(rank_seq=(2.5,), raw=1.2),
     Rank_Data(rank_seq=(2.5,), raw=1.2), Rank_Data(rank_seq=(4.0,), raw=2.3),
     Rank_Data(rank_seq=(5.0,), raw=18)]
    """
    try:
        value = next(sorted_iter)
    except StopIteration:
        # Final batch
        dups = len(same_rank_seq)
        yield from yield_sequence(
            (base+1+base+dups)/2, iter(same_rank_seq))
        return
    if key(value.raw) == key(same_rank_seq[0].raw):
        # Matching, accumulate a batch
        yield from ranker(
            sorted_iter, base, same_rank_seq+[value], key)
    else:
        # Non-matching, emit the previous batch and start a new batch
        dups = len(same_rank_seq)
        yield from yield_sequence(
            (base+1+base+dups)/2, iter(same_rank_seq))
        yield from ranker(
            sorted_iter, base+dups, [value], key)

__test__ = {
    'example': '''
>>> scalars= [0.8, 1.2, 1.2, 2.3, 18]
>>> list(rank_data(scalars))
[Rank_Data(rank_seq=(1.0,), raw=0.8), Rank_Data(rank_seq=(2.5,), raw=1.2), Rank_Data(rank_seq=(2.5,), raw=1.2), Rank_Data(rank_seq=(4.0,), raw=2.3), Rank_Data(rank_seq=(5.0,), raw=18)]
'''
}

def test():
    import doctest
    doctest.testmod(verbose=True)

if __name__ == "__main__":
    test()
