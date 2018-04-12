#!/usr/bin/env python3
"""Functional Python Programming

Chapter 16, Example Set 2

See  http://www.itl.nist.gov/div898/handbook/prc/section4/prc45.htm
"""
# pylint: disable=wrong-import-position,reimported

# Original data.
# Three rows for each shift.
# Four columns for each defect.
expected_defects = [
    [15, 21, 45, 13],
    [26, 31, 34,  5],
    [33, 17, 49, 20],
]

# Raw data reader based on qa_data.csv file.

from typing import TextIO, cast
import csv
from collections import Counter
from types import SimpleNamespace
def defect_reduce(input_file: TextIO) -> Counter:
    """
    >>> with open("qa_data.csv") as input:
    ...     defects = defect_reduce(input)
    >>> len(defects)
    12
    >>> sum(defects.values())
    309
    """
    rdr = csv.DictReader(input_file)
    assert set(rdr.fieldnames) == set(["defect_type", "serial_number", "shift"])
    rows_ns = (SimpleNamespace(**row) for row in rdr)
    defects = (
        (row.shift, row.defect_type)
        for row in rows_ns
        if row.defect_type)
    tally = Counter(defects)
    return tally

# Alternative reader based on summaries instead of details

from typing import TextIO
from collections import Counter
import csv
def defect_counts(source: TextIO) -> Counter:
    """
    >>> import io
    >>> source = io.StringIO('''shift,defect_code,count
    ... 1,A,15
    ... 2,A,26
    ... 3,A,33
    ... 1,B,21
    ... 2,B,31
    ... 3,B,17
    ... 1,C,45
    ... 2,C,34
    ... 3,C,49
    ... 1,D,13
    ... 2,D,5
    ... 3,D,20''')
    >>> defects = defect_counts(source)
    >>> len(defects)
    12
    >>> sum(defects.values())
    309
    """
    rdr = csv.DictReader(source)
    assert set(rdr.fieldnames) == set(["shift", "defect_code", "count"])
    rows_ns = (SimpleNamespace(**row) for row in rdr)
    convert = map(
        lambda d: ((d.shift, d.defect_code), int(d.count)),
        rows_ns)
    return Counter(dict(convert))

from fractions import Fraction
def chi2_eval(defects: Counter) -> Fraction:
    """
    >>> with open("qa_data.csv") as input:
    ...     defects = defect_reduce(input)
    >>> chi2 = chi2_eval(defects) #doctest: +NORMALIZE_WHITESPACE
    Total 309
    Shift Total [('1', 94), ('2', 96), ('3', 119)]
    Type Total [('A', 74), ('B', 69), ('C', 128), ('D', 38)]
    Prob(shift) of defect [('1', Fraction(94, 309)), ('2', Fraction(32, 103)), ('3', Fraction(119, 309))]
    Prob(type) of defect [('A', Fraction(74, 309)), ('B', Fraction(23, 103)), ('C', Fraction(128, 309)), ('D', Fraction(38, 309))]
    <BLANKLINE>
    Contingency Table
    obs exp    obs exp    obs exp    obs exp
     15 22.51   21 20.99   45 38.94   13 11.56   94
     26 22.99   31 21.44   34 39.77    5 11.81   96
     33 28.50   17 26.57   49 49.29   20 14.63  119
     74         69        128         38        309
    >>> chi2.limit_denominator(100)
    Fraction(1400, 73)
    """
    # pylint: disable=too-many-locals
    total = sum(defects.values())
    print(f"Total {total}")

    shift_totals = sum(
        (Counter({s: defects[s, d]}) for s, d in defects),
        Counter()  # start value is an empty Counter!
    )
    shift_detail = list(
        (s, shift_totals[s])
        for s in sorted(shift_totals)
    )
    print(f"Shift Total {shift_detail}")

    type_totals = sum(
        (Counter({d: defects[s, d]}) for s, d in defects),
        Counter()  # start value = empty Counter
    )
    type_detail = list(
        (t, type_totals[t])
        for t in sorted(type_totals))
    print(f"Type Total {type_detail}")

    P_shift = {
        shift: Fraction(shift_totals[shift], total)
        for shift in sorted(shift_totals)
    }

    P_shift_details = list(
        (s, P_shift[s]) for s in sorted(P_shift))
    print(f"Prob(shift) of defect {P_shift_details}")

    P_type = {
        type: Fraction(type_totals[type], total)
        for type in sorted(type_totals)
    }

    P_type_details = list(
        (t, P_type[t]) for t in sorted(P_type))
    print(f"Prob(type) of defect {P_type_details}")

    expected = {
        (s, t): P_shift[s]*P_type[t]*total
        for t in P_type
        for s in P_shift
    }

    print("\nContingency Table")
    print("obs exp    "*len(type_totals))
    for s in sorted(shift_totals):
        pairs = [
            f"{defects[s,t]:3d} {float(expected[s,t]):5.2f}"
            for t in sorted(type_totals)
        ]
        print(f"{'  '.join(pairs)}  {shift_totals[s]:3d}")
    footers = [
        f"{type_totals[t]:3d}      "
        for t in sorted(type_totals)]
    print(f"{'  '.join(footers)}  {total:3d}")

    # Difference

    diff = lambda e, o: (e-o)**2/e

    chi2 = sum(
        diff(expected[s, t], defects[s, t])
        for s in shift_totals
        for t in type_totals
    )
    # Cast required to narrow sum from Union[Fraction, int] to Fraction
    return cast(Fraction, chi2)

from Chapter16.ch16_ex3 import cdf

def demo():
    with open("qa_data.csv") as input_file:
        defects = defect_reduce(input_file)
    chi2 = chi2_eval(defects)
    print(f"χ² = {float(chi2):.2f}")
    print(f"χ² = {chi2.limit_denominator(50)}, P = {float(cdf(chi2, 6)):0.3%}")
    print(f"χ² = {chi2.limit_denominator(100)}, P = {cdf(chi2, 6).limit_denominator(1000)}")

def test():
    import doctest
    doctest.testmod(verbose=1)

if __name__ == "__main__":
    test()
    demo()
