#!/usr/bin/env python3

# χ² Calculation
# ==============

# ..  contents::

# The χ² table in a statistics book enumerates
# values of the χ² Cumulative Distribution Function,
# CDF.
#
# ..  math::
#
#     F(x;k) = \dfrac{\gamma \left( \frac{k}{2}, \frac{x}{2}\right)}{\Gamma\left(\frac{k}{2}\right)}
#
# See http://en.wikipedia.org/wiki/Chi-squared_distribution
#
# Given a sum-of-squares value, :math:`\chi^2`, and degrees of freedom, :math:`f`.
# We can compute :math:`p=1-F(\chi^2;k)` which is the probability of the
# :math:`\chi^2` being random.
# A value of :math:`p \leq 0.05` means the data is unlikely to be random. A value
# of :math:`p > 0.05` means that the null hypothesis is probably true:
# the data is random. The higher the :math:`p` value, the more likely that
# the null hypothesis is true.
#
# This document presents the computation of the the CDF, :math:`F(x; k)`.
# It shows a number of approaches to calculations of the two required values,
# :math:`\gamma(s,z)`, and :math:`\Gamma(t)`. A final choice for a useful
# complete gamma function is chosen based on accuracy for the given use case.
#
# See http://en.wikipedia.org/wiki/Incomplete_gamma_function#Regularized_Gamma_functions_and_Poisson_random_variables
#
# See http://en.wikipedia.org/wiki/Stirling%27s_approximation
#
# See http://dlmf.nist.gov/5 and http://dlmf.nist.gov/8
#
# See http://netlib.org/ Specifically module 542

# Imports
# -------

# Modules required by this module.

import operator
from functools import reduce, lru_cache
from fractions import Fraction
import math
from typing import Iterator, Tuple, Callable, Iterable, TypeVar

# Factorial
# -----------

# Simple integer factorial is used in a variety of places for computing
# the incomplete and complete gamma function values.

# We'll use this definition of factorial:
#
# ..  math::
#
#     n! = \prod_{i=1}^{n} i

@lru_cache(128)
def fact(k: int) -> int:
    """Simple factorial.

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
    return reduce(operator.mul, range(2,k+1))

# The implementation uses ``reduce( operator.mul, ... )`` to compute
# the product of a sequence of integer values.
# We've included the ``@lru_cache`` because this is used often,
# and the small domain of possible values leads to some benefit
# from the cache.

# We could also use ``math.factorial()``. In order to make use of
# the cache, we would need to do something like this.
#
# ..  parsed-literal::
#
#     fact = lru_cache(128)(math.factorial)
#
# This would create a similarly cached factorial function.

# Incomplete Gamma
# -----------------

# The incomplete (lower) gamma function is this:
#
# ..  math::
#
#     \gamma(s,z) = \sum_{k=0}^{\infty} \dfrac {(-1)^k} {k!} \; \dfrac {z^{s+k}} {s+k}
#

def gamma(s: float, z: float) -> float:
    """Incomplete gamma function.

    >>> import math
    >>> round(gamma(1, 2),7)
    0.8646647
    >>> round(1-math.exp(-2),7)
    0.8646647
    >>> round(gamma(1, 3),7)
    0.9502129
    >>> round(1-math.exp(-3),7)
    0.9502129
    >>> round(gamma(0.5, 2),7)
    1.6918067
    >>> round(math.sqrt(math.pi)*math.erf(math.sqrt(2)),7)
    1.6918067
    """
    
    def terms(s: float, z: float) -> Iterator[float]:
        for k in range(1000):
            term = ((-1)**k/fact(k))*(z**(s+k)/(s+k))
            yield term
    
    T_ = TypeVar("T_")        
    def take_until(function: Callable[[T_], bool], source: Iterable[T_]) -> Iterator[T_]:
        for v in source:
            if function(v): return
            yield v
    ε = 1E-8
    return sum(take_until(lambda t: abs(t) < ε, terms(s, z)))

# The idea here is to compute an infinite sequence of
# values for :math:`\dfrac {(-1)^k} {k!} \; \dfrac {z^{s+k}} {s+k}`.
# We enumerate these values while they're greater than :math:`\epsilon`.
#
# We wrote our own filter function ``take_until(end_condition, function)``.
# This stops the infinite generation of terms when the end condition
# is met.
#
# One alternative to this is a single tail-recursion, which we can  optimize
# to create a simple **for** loop which emits terms until the values are too small
# to be relevant.
#
# ..  parsed-literal::
#
#         sigma = 0
#         for k in range(1000):
#             term = ((-1)**k/fact(k))*(z**(s+k)/(s+k))
#             if abs(term) < ε: break
#             sigma += term
#         return sigma
#
# We could futher optimize this function to use stateful
# internal variables in the **for** loop. We could slightly
# improve performance with two changes.
#
# The ``(-1)**k`` expression flips the sign on each term.
# We could use, for example, ``1 if k%2 == 0 else -1``,
# which would somewhat less expensive to evaluate.
#
# Similarly, we don't really need to compute :math:`k!` for
# increasing values of *k*. We could, instead, keep a stateful running
# product calculation that we simply multiply by the next value
# of *k*.

# Gamma Function 1
# -----------------

# The various complete gamma function approxiations are all slightly
# wrong in various places. We've done three implementations
# in an attempt to locate a "best" function.
#
# The ``math.gamma()`` function is available in Python 3.2.
# We can compare this with our requirements, also.
#

# The complete gamma function has this definition:
#
# ..  math::
#
#     \Gamma(t) = \dfrac{1}{t} \prod_{k=1}^{\infty} \dfrac{\left(1+\frac{1}{k}\right)^t}{1+\frac{t}{k}}
#

def Gamma1(t: float) -> float:
    """Gamma Function.

    Gamma(n) == fact(n-1)

    >>> import math
    >>> round(Gamma1(2),0)
    1.0
    >>> round(Gamma1(3),0)
    2.0
    >>> round(Gamma1(4),0)
    6.0
    >>> round(Gamma1(5),0)
    24.0
    >>> round(Gamma1(.5), 7) # Not quite right
    1.7726754
    >>> round(math.sqrt(math.pi), 7)
    1.7724539
    """

    def num_den(t: float) -> Iterator[Tuple[float, float]]:
        for k in range(1, 1000):
            yield (1+1/k)**t, (1+t/k)

    T_ = TypeVar("T_")
    def take_until_star(
            function: Callable[[T_, T_], bool],
            source: Iterable[Tuple[T_, ...]]
        ) -> Iterable[Tuple[T_, ...]]:
        for v in source:
            if function(*v): return
            yield v

    prod = lambda x: reduce(operator.mul, x)
    fst = lambda x: x[0]
    snd = lambda x: x[1]
    ε = 1E-8

    terms = tuple(take_until_star(lambda n, d: abs(n/d-1) < ε, num_den(t)))

    return prod(map(fst, terms))/(t*prod(map(snd, terms)))

# This involves two products: the numerator product and the denominator
# product.
# The ``num_den()`` function emits an sequence of pairs, ``(n, d)``.
#
# We could consider this as a sequence of pairs like this:
#
# ..  math::
#
#     \left\langle \left(1+\frac{1}{k}\right)^t, 1+\frac{t}{k} \right\rangle
#     \textbf{ for} 1 \leq k < \infty
#
# We wrote our own filter function ``take_until_star(end_condition, function)``.
# This stops the infinite generation of tuples when the end condition for the
# tuple is met. We can't use the simple ``take_util()`` defined above because
# it makes working with tuples a little bit clunky.
# This version works more elegantly with multi-valued tuples.
#
# If the :math:`\frac{\left(1+\frac{1}{k}\right)^t}{1+\frac{t}{k}}`
# fraction is close to 1, we can stop taking values
# from the infinite iterator. We'll save this sequence in a materialized object,
# ``terms``, because we need to do two reductions on the sequence.
#
# We then split the two values in the ``terms`` sequence
# using ``fst()`` and ``snd()`` functions.
# This allows us to compute the numerator and denominator products separately.
# We defer doing the final division to the very end to
# preserve as many bits of accuracy as possible.
#
# Here's an alternative loop construction.
#
# ..  parsed-literal::
#
#     p_num = p_den = 1
#     for n in range(1,1000):
#         num, den = (1+1/n)\*\*t, (1+t/n)
#         if abs(num/den-1) < ε: break
#         p_num \*= num
#         p_den \*= den
#     return p_num/(t*p_den)
#
# Note that the value of :math:`\Gamma\left(\frac{1}{2}\right)` is very
# close to the defined value of :math:`\sqrt{\pi}`.
# The integer values, however, require rounding to zero places
# to show the expected values.

# Here's a second version using ``Fraction`` objects instead of floats.
# The idea here is to compute the **exact** value to see if -- perhaps --
# the slight discrepancies between actual and expected are due to
# float issues.

# This only works for ``int`` and ``Fraction`` values. It doesn't work
# for arbitrary ``float`` values. That's not a big limitation for this
# application.

def Gamma1f(t: float) -> float:
    """Gamma Function.

    Gamma(n) == fact(n-1)

    >>> import math
    >>> round(Gamma1f(2),0)
    Fraction(1, 1)
    >>> round(Gamma1f(3),0)
    Fraction(2, 1)
    >>> round(Gamma1f(4),0)
    Fraction(6, 1)
    >>> round(Gamma1f(5),0)
    Fraction(24, 1)
    >>> round(Gamma1f(Fraction(1,2)), 7) # Not quite right
    1.7726754
    >>> round(math.sqrt(math.pi), 7)
    1.7724539
    """

    def num_den(t: Fraction) -> Iterator[Tuple[Fraction, float]]:
        for k in range(1, 1000):
            yield (1+Fraction(1, k))**t, (1+t/k)

    T_ = TypeVar("T_")
    def take_until_star(
            function: Callable[[T_, T_], bool],
            source: Iterable[Tuple[T_, ...]]
        ) -> Iterable[Tuple[T_, ...]]:
        for v in source:
            if function(*v): return
            yield v

    prod = lambda x: reduce(operator.mul, x)
    fst = lambda x: x[0]
    snd = lambda x: x[1]
    ε = 1E-8

    t_f = Fraction(t)
    terms = tuple(take_until_star(lambda n, d: abs(n/d-1) < ε, num_den(t_f)))

    return prod(map(fst, terms))/(t_f*prod(map(snd, terms)))

# We've replaced the division operation in the ``num_den()`` function
# with ``Fraction()``. We've also replaced the argument value, ``t``,
# with a ``Fraction``, ``t_f``.
#
# Two other divisions were left in place because the arguments would be
# ``Fraction`` instances:
#
# -  In the ``num_den()`` function, we left a division because the argument,
#    ``t`` will be a ``Fraction``.
#
# -  The final division (betweem two ``Fraction`` objects) is left in place.
#
# Interestingly, this produces essentially the same results as the previous
# version. This, too, is not very accurate for values near :math:``\frac{1}{2}``.

# Gamma Function 2
# ------------------

# It's not clear that we can do better than ``gamma1()``, but it's worth looking
# at other alternatives. The Nemes approximation has the
# advantage of brevity.
#
# ..  math::
#
#     \Gamma(z) \sim \sqrt{ \frac{2\pi}{z} } \left( \frac{1}{e} \left(z+\frac{1}{12z-\frac{1}{10z}} \right) \right)^z
#

def Gamma2(z: float) -> float:
    """Gamma Function. Gergő Nemes version.

    Gamma(n) == fact(n-1)

    >>> import math
    >>> round(Gamma2(2),1)
    1.0
    >>> round(Gamma2(3),1)
    2.0
    >>> round(Gamma2(4),1)
    6.0
    >>> round(Gamma2(5),1)
    24.0
    >>> round(Gamma2(.5), 7) # Not quite right
    1.7630962
    >>> round(math.sqrt(math.pi), 7)
    1.7724539
    """
    t_1 = math.sqrt(2*math.pi/z)
    t_2 = (z+(1/(12*z-(1/(10*z)))))/math.e
    return t_1*t_2**z

# We broke the expression into two parts just to shorten up the
# expression.
#
# ..  math::
#
#     t_1 &= \sqrt{ \frac{2\pi}{z} } \\
#     t_2 &= \frac{\left(z+\frac{1}{12z-\frac{1}{10z}} \right)}{e} \\
#     \Gamma(z) &= {t_1} \times {t_2}^z
#

# This is a simple, closed-form evaluation of a function.
# It's remarkably inaccurate for :math:`\Gamma \left( \dfrac{1}{2} \right)`.
# For integer values, however, it's very good.

# Gamma Function 3
# -------------------

# Here's the Sterling version. This sums a sequence of values.
#
# ..  math::
#
#     \Gamma(z) \sim e^{-z}z^z \sqrt{ \frac{2\pi}{z} } \left( \sum_{k=0}^\infty \dfrac{g_k} {z^k} \right)
#
# Here is the beginning of the sequence of :math:`g_k` values.
#
# ..    math::
#
#       g_0	&=1,	\\
#       g_1	&=1/12,	\\
#       g_2	&=1/288,	\\
#       g_3	&=−139/51840,	\\
#       g_4	&=−571/24\,88320,	\\
#       g_5	&=1\,63879/2090\,18880,	\\
#       g_6	&=52\,46819/7\,52467\,96800.
#
# There's a defined rule for calculating these obscure-looking values.
# However, we note that the last of these is near ``10E-5``, this is enough
# to give us a usefully accurate answer.

# This is not a convergent series: using more terms used may actually *reduce*
# the accuracy of the approximation. For the values we're working with,
# we don't seem to need all six terms shown above.

def Gamma3(z: float) -> float:
    """Gamma Function. Sterling version.

    http://dlmf.nist.gov/5.11#E3

    Gamma(n) == fact(n-1)

    >>> import math
    >>> round(Gamma3(2),1)
    1.0
    >>> round(Gamma3(3),1)
    2.0
    >>> round(Gamma3(4),1)
    6.0
    >>> round(Gamma3(5),1)
    24.0
    >>> round(Gamma3(.5), 7)
    1.7737381
    >>> round(math.sqrt(math.pi), 7)
    1.7724539
    """
    t_1 = math.exp(-z)*z**z
    t_2 = math.sqrt(2*math.pi/z)
    g = [1, 1/12, 1/288, -139/51840, -571/2488320, 163879/209018880, 5246819/75246796800]
    t_3 = sum(g[k]/(z**k) for k in range(2))
    return t_1*t_2*t_3

# We've broken this into three parts, to reduce the size of the overall
# expression.
#
# ..  math::
#
#     t_1 &= e^{-z}z^z \\
#     t_2 &= \sqrt{ \frac{2\pi}{z} } \\
#     t_3 &= \sum_{k=0}^\infty \dfrac{g_k} {z^k} \\
#     \Gamma(z) &= t_1 \times t_2 \times t_3
#
# This is acceptable for :math:`\Gamma \left( \dfrac{1}{2} \right)`.
# Note that we're only using the first two terms. Compare these results with the
# ``Gamma2()`` function, shown above. The number of terms required seems
# to vary with the range of the vaue of :math:`z`.

# Gamma Hybrid
# -------------

# Most of the approximations aren't very accurate
# for the :math:`\Gamma\left(\frac{k}{2}\right)` values.
# We can use this exact closed-form expression instead:
#
# ..  math::
#
#     \Gamma\left(\frac{1}{2}+n\right) = \frac{(2n)!}{4^n n!}\sqrt{\pi}
#
# This provides precise values for the special cases we're using.

# Here's a hybrid ``Gamma()`` function. For certain values, we'll use the exact
# :math:`\Gamma\left(\frac{1}{2}+n\right)` value. For other values,
# we'll use the ``Gamma2()`` approximation, above.

def Gamma_Half(k: float) -> float:
    """Gamma(k) with special case for k = n+1/2; k-1/2=n.

    >>> import math
    >>> round(Gamma_Half(2),1)
    1.0
    >>> round(Gamma_Half(3),1)
    2.0
    >>> round(Gamma_Half(4),1)
    6.0
    >>> round(Gamma_Half(5),1)
    24.0

    >>> round(Gamma_Half(.5), 7)
    1.7724539
    >>> round(math.sqrt(math.pi), 7)
    1.7724539
    >>> round(Gamma_Half(1.5), 7)
    0.8862269
    >>> round(math.sqrt(math.pi)/2, 7)
    0.8862269
    """
    ε = 1E-6
    if abs(k-int(k)-.5) < ε:
        n = int(k-.5)
        return fact(2*n)/(4**n*fact(n))*math.sqrt(math.pi)
    else:
        return float(Gamma2(k))

# If the value is an :math:`n+\dfrac{1}{2} \pm \epsilon`, we'll use the special
# close-form expression. If the value is not close to :math:`n+\dfrac{1}{2}`,
# we'll use a more general approximation.

# The math.gamma() Version
# ---------------------------

# Here's a test case for the ``math.gamma()`` function.

test_math_gamma = """
>>> import math
>>> round(math.gamma(2),2)
1.0
>>> round(math.gamma(3),2)
2.0
>>> round(math.gamma(4),2)
6.0
>>> round(math.gamma(5),2)
24.0

>>> round(math.gamma(.5), 7)
1.7724539
>>> round(math.sqrt(math.pi), 7)
1.7724539
>>> round(math.gamma(1.5), 7)
0.8862269
>>> round(math.sqrt(math.pi)/2, 7)
0.8862269
"""

# This looks good, also. For the given test cases, it's as accurate
# as our hybrid shown above.

# Cumulative Distribution Function
# ==================================

# The real calculation of the CDF from a :math:`\chi^2` value, ``x``, and
# the degrees of freedom, ``k``.

def cdf(x: float, k: int) -> float:
    """χ² cumulative distribution function.

    :param x: χ² value -- generally sum (obs[i]-exp[i])**2/exp[i]
        for parallel sequences of observed and expected values.
    :param k: degrees of freedom >= 1; generally len(data)-1

    From http://en.wikipedia.org/wiki/Chi-squared_distribution

    >>> round(cdf(0.004, 1), 2)
    0.95
    >>> round(cdf(10.83, 1), 3)
    0.001
    >>> round(cdf(3.94, 10), 2)
    0.95
    >>> round(cdf(29.59, 10), 3)
    0.001
    >>> expected=[0.95, 0.90, 0.80, 0.70, 0.50, 0.30, 0.20, 0.10, 0.05, 0.01, 0.001]
    >>> chi2= [0.004, 0.02, 0.06, 0.15, 0.46, 1.07, 1.64, 2.71, 3.84, 6.64, 10.83]
    >>> act= [round(x,3) for x in map(cdf, chi2, [1]*len(chi2))]
    >>> act
    [0.95, 0.888, 0.806, 0.699, 0.498, 0.301, 0.2, 0.1, 0.05, 0.01, 0.001]

    From http://www.itl.nist.gov/div898/handbook/prc/section4/prc45.htm

    >>> round(cdf(19.18, 6), 5)
    0.00387
    >>> round(cdf(12.5916, 6), 2)
    0.05

    From http://www.itl.nist.gov/div898/handbook/prc/section4/prc46.htm
    >>> round(cdf(12.131, 4), 5)
    0.01639
    >>> round(cdf(9.488, 4), 2)
    0.05

    """
    return 1-gamma(k/2, x/2)/Gamma_Half(k/2)

# The calcuation is 1 minus the ratio the partial
# gamma to the full gamma.

# Unit Test Cases
# ===============

# We'll use the doctest comments in each function defined above.
# Additionally, we'll use some strings with doctest test cases.

__test__ = {
    "test_math_gamma": test_math_gamma,
}

def test(*args, **kw):
    import doctest
    doctest.testmod(*args, **kw)

if __name__ == "__main__":
    test()
