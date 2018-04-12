#!/usr/bin/env python3
"""Functional Python Programming

Chapter 16, Example Set 3
"""
# pylint: disable=wrong-import-position

from functools import lru_cache, reduce
import operator
from fractions import Fraction
import warnings

@lru_cache(128)
def fact(k: int) -> int:
    """Simple factorial of a Fraction or an int.

    >>> fact(1)
    1
    >>> fact(2)
    2
    >>> fact(3)
    6
    >>> fact(4)
    24
    """
    if k < 2:
        return 1
    return reduce(operator.mul, range(2, int(k)+1))

from typing import Iterator, Iterable, Callable, cast
def gamma(s: Fraction, z: Fraction) -> Fraction:
    """Incomplete gamma function.

    >>> import math
    >>> round(float(gamma(1, 2)),7)
    0.8646647
    >>> round(1-math.exp(-2),7)
    0.8646647
    >>> round(float(gamma(1, 3)),7)
    0.9502129
    >>> round(1-math.exp(-3),7)
    0.9502129
    >>> round(float(gamma(Fraction(1,2), Fraction(2))),7)
    1.6918067
    >>> round(math.sqrt(math.pi)*math.erf(math.sqrt(2)),7)
    1.6918067
    >>> g= gamma(Fraction(1,2), Fraction(2)).limit_denominator(1000000)
    >>> g
    Fraction(144438, 85375)
    >>> round(float(g),7)
    1.6918067
    """
    def terms(s: Fraction, z: Fraction) -> Iterator[Fraction]:
        """Terms for computing partial gamma"""
        for k in range(100):
            t2 = Fraction(z**(s+k))/(s+k)
            term = Fraction((-1)**k, fact(k))*t2
            yield term
        warnings.warn("More than 100 terms")
    def take_until(function: Callable[..., bool], source: Iterable) -> Iterator:
        """Take from source until function is false."""
        for v in source:
            if function(v):
                return
            yield v
    ε = 1E-8
    g = sum(take_until(lambda t: abs(t) < ε, terms(s, z)))
    # cast required to narrow sum from Union[Fraction, int] to Fraction
    return cast(Fraction, g)

pi = Fraction(5_419_351, 1_725_033)
# Fraction(817_696_623, 260_280_919)

sqrt_pi = Fraction(677_622_787, 382_307_718)
# Fraction(582_540, 328_663) # Good for almost all test cases but one.

from typing import Union
def Gamma_Half(k: Union[int, Fraction]) -> Union[int, Fraction]:
    """Gamma(k) with special case for k = n+1/2; k-1/2=n.

    >>> import math
    >>> Gamma_Half(2)
    1
    >>> Gamma_Half(3)
    2
    >>> Gamma_Half(4)
    6
    >>> Gamma_Half(5)
    24

    >>> g= Gamma_Half(Fraction(1,2)) # Varies with sqrt_pi setting
    >>> g.limit_denominator(2_000_000)
    Fraction(582540, 328663)
    >>> round(float(g), 7)
    1.7724539
    >>> round(math.sqrt(math.pi), 7)
    1.7724539
    >>> g= Gamma_Half(Fraction(3,2)) # Varies with sqrt_pi setting
    >>> g.limit_denominator(2_000_000)
    Fraction(291270, 328663)
    >>> round(float(g), 7)
    0.8862269
    >>> round(math.sqrt(math.pi)/2, 7)
    0.8862269
    """
    if isinstance(k, int):
        return fact(k-1)
    elif isinstance(k, Fraction):
        if k.denominator == 1:
            return fact(k-1)
        elif k.denominator == 2:
            n = k-Fraction(1, 2)
            return fact(2*n)/(Fraction(4**n)*fact(n))*sqrt_pi
    raise ValueError(f"Can't compute Γ({k})")

def cdf(x: Union[Fraction, float], k: int) -> Fraction:
    """χ² cumulative distribution function.

    :param x: χ² value -- generally sum(obs[i]-exp[i])**2/exp[i]
        for parallel sequences of observed and expected values.
    :param k: degrees of freedom >= 1; generally len(data)-1

    From http://en.wikipedia.org/wiki/Chi-squared_distribution

    >>> round(float(cdf(0.004, 1)), 2)
    0.95
    >>> cdf(0.004, 1).limit_denominator(100)
    Fraction(94, 99)
    >>> round(float(cdf(10.83, 1)), 3)
    0.001
    >>> cdf(10.83, 1).limit_denominator(1000)
    Fraction(1, 1000)
    >>> round(float(cdf(3.94, 10)), 2)
    0.95
    >>> cdf(3.94, 10).limit_denominator(100)
    Fraction(19, 20)
    >>> round(float(cdf(29.59, 10)), 3)
    0.001
    >>> cdf(29.59, 10).limit_denominator(10000)
    Fraction(8, 8005)
    >>> expected = [0.95, 0.90, 0.80, 0.70, 0.50, 0.30, 0.20, 0.10, 0.05, 0.01, 0.001]
    >>> chi2 = [0.004, 0.02, 0.06, 0.15, 0.46, 1.07, 1.64, 2.71, 3.84, 6.64, 10.83]
    >>> act = [round(float(x), 3)
    ...     for x in map(cdf, chi2, [1]*len(chi2))]
    >>> act
    [0.95, 0.888, 0.806, 0.699, 0.498, 0.301, 0.2, 0.1, 0.05, 0.01, 0.001]

    From http://www.itl.nist.gov/div898/handbook/prc/section4/prc45.htm

    >>> round(float(cdf(19.18, 6)), 5)
    0.00387
    >>> round(float(cdf(12.5916, 6)), 2)
    0.05
    >>> cdf(19.18, 6).limit_denominator(1000)
    Fraction(3, 775)

    From http://www.itl.nist.gov/div898/handbook/prc/section4/prc46.htm

    >>> round(float(cdf(12.131, 4)), 5) # 0.01639 shown in reference
    0.0164
    >>> cdf(12.131, 4).limit_denominator(1000)
    Fraction(16, 975)
    >>> round(float(cdf(9.488, 4)), 2)
    0.05
    >>> cdf(9.488, 4).limit_denominator(1000)
    Fraction(1, 20)
    """
    return 1-gamma(Fraction(k, 2), Fraction(x/2))/Gamma_Half(Fraction(k, 2))
    #return 1-gamma(Fraction(k,2), Fraction(x/2).limit_denominator(1000))/Gamma_Half(Fraction(k,2))

def test():
    import doctest
    doctest.testmod(verbose=1)

if __name__ == "__main__":
    test()
