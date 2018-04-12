#!/usr/bin/env python3
"""Functional Python Programming

Chapter 7, Example Set 3
"""
#pylint: disable=wrong-import-order,wrong-import-position,reimported

import Chapter04.ch04_ex4

# Raw Data Parser

# from collections import namedtuple
# Pair = namedtuple("Pair", ("x", "y"))

from typing import NamedTuple
class Pair(NamedTuple):
    x: float
    y: float

from typing import Iterator, Iterable, Sequence
def head_reader(
        rows: Iterator[Sequence[str]]
    ) -> Iterator[Sequence[str]]:
    """Consumes three header rows and returns the iterator."""
    r0 = next(rows)
    r1 = next(rows)
    r2 = next(rows)
    assert set(r2) == {"x", "y"}, set(r2)
    return rows

def tail_reader(
        rows: Iterable[Sequence[str]]
    ) -> Iterator[Sequence[float]]:
    return (tuple(map(float, row)) for row in rows)

def series(
        n: int,
        row_iter: Iterable[Sequence[float]]
    ) -> Iterator[Pair]:
    return (Pair(*row[2*n:2*n+2]) for row in row_iter)

# Rank Correlation

from collections import defaultdict

from typing import Callable, Tuple, List, TypeVar, cast, Dict
D_ = TypeVar("D_")
K_ = TypeVar("K_")
def rank(
        data: Iterable[D_],
        key: Callable[[D_], K_] = lambda obj: cast(K_, obj)
    ) -> Iterator[Tuple[float, D_]]:
    """Yield the data rank ordered by the given key.
    Creates a defaultdict(list) in order to discover duplicates.
    This is a similar to a Counter, but it keeps details and
    it uses a key function.

    >>> list(rank( [0.8, 1.2, 1.2, 2.3, 18] ) )
    [(1.0, 0.8), (2.5, 1.2), (2.5, 1.2), (4.0, 2.3), (5.0, 18)]
    >>> data= ((2, 0.8), (3, 1.2), (5, 1.2), (7, 2.3), (11, 18))
    >>> list(rank( data, key=lambda x:x[1] ))
    [(1.0, (2, 0.8)), (2.5, (3, 1.2)), (2.5, (5, 1.2)), (4.0, (7, 2.3)), (5.0, (11, 18))]
    """

    def rank_output(
            duplicates: Dict[K_, List[D_]],
            key_iter: Iterator[K_],
            base: int = 0
        ) -> Iterator[Tuple[float, D_]]:
        for k in key_iter:
            dups = len(duplicates[k])
            for value in duplicates[k]:
                yield (base+1+base+dups)/2, value
            base += dups

    # Alternative: Properly recursive version of the rank_output loop
    # pylint: disable=pointless-string-statement
    """
    def rank_output(duplicates, key_iter, base=0):
        k = next(key_iter)
        dups = len(duplicates[k])
        for value in duplicates[k]:
            yield (base+1+base+dups)/2, value
        yield from rank_output(duplicates, key_iter, base+dups)
    """

    def build_duplicates(
            duplicates: Dict[K_, List[D_]],
            data_iter: Iterator[D_],
            key: Callable[[D_], K_]
        ) -> Dict[K_, List[D_]]:
        for item in data_iter:
            duplicates[key(item)].append(item)
        return duplicates

    # Need a properly recursive way to build the dict(list) structure.
    duplicates = build_duplicates(defaultdict(list), iter(data), key)
    return rank_output(duplicates, iter(sorted(duplicates)), 0)

from typing import Sequence
def rank2_imp(
        data: Sequence[D_],
        key: Callable[[D_], K_] = lambda x: cast(K_, x)
    ) -> Iterator[Tuple[float, D_]]:
    """
    Alternative rank using a stateful queue object: optimized version.

    >>> list(rank2_imp( [0.8, 1.2, 1.2, 2.3, 18] ) )
    [(1.0, 0.8), (2.5, 1.2), (2.5, 1.2), (4.0, 2.3), (5.0, 18)]
    >>> data= ((2, 0.8), (3, 1.2), (5, 1.2), (7, 2.3), (11, 18))
    >>> list(rank2_imp( data, key=lambda x:x[1] ))
    [(1.0, (2, 0.8)), (2.5, (3, 1.2)), (2.5, (5, 1.2)), (4.0, (7, 2.3)), (5.0, (11, 18))]
    """
    data_iter = iter(sorted(data, key=key))
    base = 0
    same_rank = [next(data_iter)]  # Queue().append(data_iter)
    for value in data_iter:
        if key(value) == key(same_rank[0]):
            same_rank.append(value)  # or same_rank += [value]
        else:
            dups = len(same_rank)
            for dup_rank_item in same_rank:  # same_rank.pop()
                yield (base+1+base+dups)/2, dup_rank_item
            base += dups
            same_rank = [value]  # same_rank.append()
    dups = len(same_rank)
    for value in same_rank:  # same_rank.pop()
        yield (base+1+base+dups)/2, value

def rank2_rec(
        data: Sequence[D_],
        key: Callable[[D_], K_] = lambda x: cast(K_, x)
    ) -> Iterator[Tuple[float, D_]]:
    """
    Alternative rank without a Counter object.
    Closer to properly recursive version.

    >>> list(rank2_rec( [0.8, 1.2, 1.2, 2.3, 18] ) )
    [(1.0, 0.8), (2.5, 1.2), (2.5, 1.2), (4.0, 2.3), (5.0, 18)]
    >>> data= ((2, 0.8), (3, 1.2), (5, 1.2), (7, 2.3), (11, 18))
    >>> list(rank2_rec( data, key=lambda x:x[1] ))
    [(1.0, (2, 0.8)), (2.5, (3, 1.2)), (2.5, (5, 1.2)), (4.0, (7, 2.3)), (5.0, (11, 18))]
    """
    def yield_sequence(
            rank: float,
            same_rank_iter: Iterator[D_]
        ) -> Iterator[Tuple[float, D_]]:
        head = next(same_rank_iter)
        yield rank, head
        yield from yield_sequence(rank, same_rank_iter)

    def ranker(
            sorted_iter: Iterator[D_],
            base: int,
            same_rank_list: List[D_]
        ) -> Iterator[Tuple[float, D_]]:
        try:
            value = next(sorted_iter)
        except StopIteration:
            dups = len(same_rank_list)
            yield from yield_sequence((base+1+base+dups)/2, iter(same_rank_list))
            return
        if key(value) == key(same_rank_list[0]):
            yield from ranker(sorted_iter, base, same_rank_list+[value])
        else:
            dups = len(same_rank_list)
            yield from yield_sequence((base+1+base+dups)/2, iter(same_rank_list))
            for rows in ranker(sorted_iter, base+dups, [value]):
                yield rows

    data_iter = iter(sorted(data, key=key))
    head = next(data_iter)
    yield from ranker(data_iter, 0, [head])

# Ranked_Y = namedtuple("Ranked_Y", ("r_y", "raw",))

from typing import NamedTuple
class Ranked_Y(NamedTuple):
    r_y: float
    raw: Pair

def rank_y(pairs: Iterable[Pair]) -> Iterable[Ranked_Y]:
    """
    Partial rank ordering of a data set by the y member of each pair.

    >>> data = (Pair(x=10.0, y=8.04), Pair(x=8.0, y=6.95),
    ... Pair(x=13.0, y=7.58), Pair(x=9.0, y=8.81), Pair(x=11.0, y=8.33),
    ... Pair(x=14.0, y=9.96), Pair(x=6.0, y=7.24), Pair(x=4.0, y=4.26),
    ... Pair(x=12.0, y=10.84), Pair(x=7.0, y=4.82), Pair(x=5.0, y=5.68))
    >>> list(rank_y(data))  # doctest: +NORMALIZE_WHITESPACE
    [Ranked_Y(r_y=1.0, raw=Pair(x=4.0, y=4.26)),
     Ranked_Y(r_y=2.0, raw=Pair(x=7.0, y=4.82)),
     Ranked_Y(r_y=3.0, raw=Pair(x=5.0, y=5.68)),
     Ranked_Y(r_y=4.0, raw=Pair(x=8.0, y=6.95)),
     Ranked_Y(r_y=5.0, raw=Pair(x=6.0, y=7.24)),
     Ranked_Y(r_y=6.0, raw=Pair(x=13.0, y=7.58)),
     Ranked_Y(r_y=7.0, raw=Pair(x=10.0, y=8.04)),
     Ranked_Y(r_y=8.0, raw=Pair(x=11.0, y=8.33)),
     Ranked_Y(r_y=9.0, raw=Pair(x=9.0, y=8.81)),
     Ranked_Y(r_y=10.0, raw=Pair(x=14.0, y=9.96)),
     Ranked_Y(r_y=11.0, raw=Pair(x=12.0, y=10.84))]
    """
    return (
        Ranked_Y(rank, data)
        for rank, data in rank(pairs, lambda pair: pair.y)
    )

# Ranked_XY = namedtuple("Ranked_XY", ("r_x", "r_y", "raw",))
class Ranked_XY(NamedTuple):
    r_x: float
    r_y: float
    raw: Pair

def rank_xy(pairs: Sequence[Pair]) -> Iterator[Ranked_XY]:
    """
    Two-pass rank ordering by the x and y members of each pair.
    An intermediate sequence of Rank_Y objects are created with partial
    rankings. The result are Rank_XY objects.

    >>> data = (Pair(x=10.0, y=8.04), Pair(x=8.0, y=6.95),
    ... Pair(x=13.0, y=7.58), Pair(x=9.0, y=8.81), Pair(x=11.0, y=8.33),
    ... Pair(x=14.0, y=9.96), Pair(x=6.0, y=7.24), Pair(x=4.0, y=4.26),
    ... Pair(x=12.0, y=10.84), Pair(x=7.0, y=4.82), Pair(x=5.0, y=5.68))
    >>> list(rank_xy(data))  # doctest: +NORMALIZE_WHITESPACE
    [Ranked_XY(r_x=1.0, r_y=1.0, raw=Pair(x=4.0, y=4.26)),
     Ranked_XY(r_x=2.0, r_y=3.0, raw=Pair(x=5.0, y=5.68)),
     Ranked_XY(r_x=3.0, r_y=5.0, raw=Pair(x=6.0, y=7.24)),
     Ranked_XY(r_x=4.0, r_y=2.0, raw=Pair(x=7.0, y=4.82)),
     Ranked_XY(r_x=5.0, r_y=4.0, raw=Pair(x=8.0, y=6.95)),
     Ranked_XY(r_x=6.0, r_y=9.0, raw=Pair(x=9.0, y=8.81)),
     Ranked_XY(r_x=7.0, r_y=7.0, raw=Pair(x=10.0, y=8.04)),
     Ranked_XY(r_x=8.0, r_y=8.0, raw=Pair(x=11.0, y=8.33)),
     Ranked_XY(r_x=9.0, r_y=11.0, raw=Pair(x=12.0, y=10.84)),
     Ranked_XY(r_x=10.0, r_y=6.0, raw=Pair(x=13.0, y=7.58)),
     Ranked_XY(r_x=11.0, r_y=10.0, raw=Pair(x=14.0, y=9.96))]
    """
    return (
        Ranked_XY(r_x=r_x, r_y=rank_y_raw[0], raw=rank_y_raw[1])
        for r_x, rank_y_raw in rank(rank_y(pairs), lambda r: r.raw.x)
    )

def rank_corr(pairs: Sequence[Pair]) -> float:
    """Spearman rank correlation.
    >>> data = [Pair(x=86.0, y=0.0), Pair(x=97.0, y=20.0),
    ... Pair(x=99.0, y=28.0), Pair(x=100.0, y=27.0), Pair(x=101.0, y=50.0),
    ... Pair(x=103.0, y=29.0), Pair(x=106.0, y=7.0), Pair(x=110.0, y=17.0),
    ... Pair(x=112.0, y=6.0), Pair(x=113.0, y=12.0)]
    >>> round(rank_corr( data ), 9)
    -0.175757576
    >>> data = (Pair(x=10.0, y=8.04), Pair(x=8.0, y=6.95),
    ... Pair(x=13.0, y=7.58), Pair(x=9.0, y=8.81), Pair(x=11.0, y=8.33),
    ... Pair(x=14.0, y=9.96), Pair(x=6.0, y=7.24), Pair(x=4.0, y=4.26),
    ... Pair(x=12.0, y=10.84), Pair(x=7.0, y=4.82), Pair(x=5.0, y=5.68))
    >>> round(rank_corr( data ), 3)
    0.818

    Note that Pearson R for Anscombe data set I is 0.816.
    The difference, while small, is significant.

    >>> hgt_mass = (Pair(x=1.47, y=52.21),
    ... Pair(x=1.5, y=53.12), Pair(x=1.52, y=54.48), Pair(x=1.55, y=55.84),
    ... Pair(x=1.57, y=57.2), Pair(x=1.6, y=58.57), Pair(x=1.63, y=59.93),
    ... Pair(x=1.65, y=61.29), Pair(x=1.68, y=63.11), Pair(x=1.7, y=64.47),
    ... Pair(x=1.73, y=66.28), Pair(x=1.75, y=68.1), Pair(x=1.78, y=69.92),
    ... Pair(x=1.8, y=72.19), Pair(x=1.83, y=74.46))
    >>> round(rank_corr( hgt_mass ), 3)
    1.0
    """
    ranked = rank_xy(pairs)
    sum_d_2 = sum((r.r_x - r.r_y)**2 for r in ranked)
    n = len(pairs)
    return 1-6*sum_d_2/(n*(n**2-1))

def pearson_corr(pairs: Sequence[Pair]) -> float:
    """Pearson correlation of Pairs.

    >>> data = (Pair(x=10.0, y=8.04), Pair(x=8.0, y=6.95),
    ... Pair(x=13.0, y=7.58), Pair(x=9.0, y=8.81),
    ... Pair(x=11.0, y=8.33), Pair(x=14.0, y=9.96),
    ... Pair(x=6.0, y=7.24), Pair(x=4.0, y=4.26),
    ... Pair(x=12.0, y=10.84), Pair(x=7.0, y=4.82),
    ... Pair(x=5.0, y=5.68))
    >>> round(pearson_corr( data ), 3)
    0.816

    >>> hgt_mass= (Pair(x=1.47, y=52.21), Pair(x=1.5, y=53.12),
    ... Pair(x=1.52, y=54.48), Pair(x=1.55, y=55.84), Pair(x=1.57, y=57.2),
    ... Pair(x=1.6, y=58.57), Pair(x=1.63, y=59.93), Pair(x=1.65, y=61.29),
    ... Pair(x=1.68, y=63.11), Pair(x=1.7, y=64.47), Pair(x=1.73, y=66.28),
    ... Pair(x=1.75, y=68.1), Pair(x=1.78, y=69.92), Pair(x=1.8, y=72.19),
    ... Pair(x=1.83, y=74.46))
    >>> round(pearson_corr( hgt_mass ), 5)
    0.99458
    """
    X = tuple(p.x for p in pairs)
    Y = tuple(p.y for p in pairs)
    return Chapter04.ch04_ex4.corr(X, Y)

test_all = """
>>> import csv
>>> from io import StringIO
>>> Anscombe = '''\
... Anscombe's quartet
... I\\tII\\tIII\\tIV
... x\\ty\\tx\\ty\\tx\\ty\\tx\\ty
... 10.0\\t8.04\\t10.0\\t9.14\\t10.0\\t7.46\\t8.0\\t6.58
... 8.0\\t6.95\\t8.0\\t8.14\\t8.0\\t6.77\\t8.0\\t5.76
... 13.0\\t7.58\\t13.0\\t8.74\\t13.0\\t12.74\\t8.0\\t7.71
... 9.0\\t8.81\\t9.0\\t8.77\\t9.0\\t7.11\\t8.0\\t8.84
... 11.0\\t8.33\\t11.0\\t9.26\\t11.0\\t7.81\\t8.0\\t8.47
... 14.0\\t9.96\\t14.0\\t8.10\\t14.0\\t8.84\\t8.0\\t7.04
... 6.0\\t7.24\\t6.0\\t6.13\\t6.0\\t6.08\\t8.0\\t5.25
... 4.0\\t4.26\\t4.0\\t3.10\\t4.0\\t5.39\\t19.0\\t12.50
... 12.0\\t10.84\\t12.0\\t9.13\\t12.0\\t8.15\\t8.0\\t5.56
... 7.0\\t4.82\\t7.0\\t7.26\\t7.0\\t6.42\\t8.0\\t7.91
... 5.0\\t5.68\\t5.0\\t4.74\\t5.0\\t5.73\\t8.0\\t6.89
... '''
>>> with StringIO(Anscombe) as source:
...        rdr= csv.reader( source, delimiter='\\t' )
...        data= tuple(tail_reader( head_reader(rdr) ))
...        s_I= tuple(series(0, data))
...        s_II= tuple(series(1, data))
...        s_III= tuple(series(2, data))
...        s_IV= tuple(series(3, data))
>>> print( "Set {0:>4s}, {1:.3f}, {2:.3f}".format(
...        "I", rank_corr( s_I ), pearson_corr( s_I ) ) )
Set    I, 0.818, 0.816
>>> print( "Set {0:>4s}, {1:.3f}, {2:.3f}".format(
...        "II", rank_corr( s_II ), pearson_corr( s_II ) ) )
Set   II, 0.691, 0.816
>>> print( "Set {0:>4s}, {1:.3f}, {2:.3f}".format(
...        "III", rank_corr( s_III ), pearson_corr( s_III ) ) )
Set  III, 0.991, 0.816
>>> print( "Set {0:>4s}, {1:.3f}, {2:.3f}".format(
...     "IV", rank_corr( s_IV ), pearson_corr( s_IV ) ) )
Set   IV, 0.625, 0.817
"""

__test__ = {
    "test_all": test_all,
}

if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True)
