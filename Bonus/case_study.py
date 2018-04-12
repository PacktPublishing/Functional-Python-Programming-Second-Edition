#!/usr/bin/env python3

# Statistics Case Study
# =====================

# This is a case study of using χ² in an EDA context.
# See  http://www.itl.nist.gov/div898/handbook/prc/section4/prc45.htm

# Here's the background information from this example:

#     A total of 309 wafer defects were recorded and the defects
#     were classified as being one of four types, A, B, C, or D.
#     At the same time each wafer was identified according to
#     the production shift in which it was manufactured, 1, 2, or 3.

# We have a table of defects by shift and type. Each row is a different
# shift, each column is a different type.

defects = [
    [15, 21, 45, 13],
    [26, 31, 34,  5],
    [33, 17, 49, 20],
]

# We can imagine this is the result of summarizing raw data.
# The raw data migth look like this:
#
# ..    parsed-literal::
#
#       shift,defect,serial
#       1,None,12345
#       1,None,12346
#       1,A,12347
#       1,B,12348
#       *etc.* for thousands of wafers
#
# The summary table is the result of something like a
# ``collections.Counter()`` using ``shift,defect`` as the key.
#
# Or perhaps the results come from a SQL query like this:
#
# ..    parsed-literal::
#
#       SELECT SHIFT, DEFECT, COUNT(*) FROM some tables
#       ...
#       GROUP BY SHIFT, DEFECT
#       HAVING DEFECT NOT NULL;
#

# Before starting the analysis, we'll need to import some libraries

from chi_sq import cdf
from fractions import Fraction

# Basic EDA Analysis
# ------------------

# We need to see if the effects are random or not. If the effects are
# random variation, our hypothesis is that there's nothing to see
# here. This is the statistician's "null hypothesis:" nothing interesting
# is happening.
#
# To evaluate the null hypothesis, we compare the observed defect
# data against some reasonable expectations for the defect data.
#
# What we'll do is determine a hypothetical allocation of the
# same total number of defects that has a similar distribution
# based on shift and type.
#
# The total number of defects is :math:`\sum_s \sum_t d_{s,t} = 309`.

total = sum(map(sum, defects))

# We need to compute expected defects by shift and type.
# The null hypothesis asserts that all effects are random,
# so the efects should be evenly spread across shift and type.

# Defects By Shift
# ---------------------

# The shift totals are defined as :math:`\lbrace \sum_t d_{st} \bigl\vert 0 \leq s < 3 \rbrace`.

shift_total = [sum(defects[s][t] for t in range(4)) for s in range(3)]

# The total number of defects by shift are ``[94, 96, 119]``.
#
# We can also calculate the totals like this, but that doesn't generalize well
# to for computing sum across types.
#
# ..    parsed-literal::
#
#       list(map(sum, defects))
#
# Here are the probabilities of a defect based on actual counts
# of defects by shift.

P_shift = [Fraction(s,total) for s in shift_total]

# We get this as a value ``[Fraction(94, 309), Fraction(32, 103), Fraction(119, 309)]``.

# We've materialized two list objects here. Since we'll be producing some
# intermediate output, the materialized collections are helpful.
# If we did not intend to produce intermediate output, we could use
# lazy generator functions to reduce the amount of memory required.

# Defects By Type
# ---------------------------

# Computing the type totals isn't quite so simple as computing the
# shift totals because we're slicing the matrix on an axis that doesn't
# work trivially with the ``sum()`` function.
#
# Here are the type totals: :math:`\lbrace \sum_s d_{st} \bigl\vert 0 \leq t < 4 \rbrace`.

type_total = [sum(shift[t] for shift in defects) for t in range(4)]

# The values are ``[74, 69, 128, 38]``.
#
# Here are the probabilities of a defect based on actual counts
# of defects by type.

P_type = [Fraction(t,total) for t in type_total]

# The values are ``[Fraction(74, 309), Fraction(23, 103), Fraction(128, 309), Fraction(38, 309)]``.

# Combined Expectations
# ---------------------

# The overall defect probabilities
# are :math:`P_{ij} = Ps_s \times Pt_t` for each shift
# and type. This reflects the null hypothesis that neither shift nor type
# of defect has any bearing on the values: they're all just random.
#
# We can multiplie the probability by the total number of defects to compute
# how many defects belong to each combination of shift and type.

expected = [
    [float(ps*pt)*total for pt in P_type]
    for ps in P_shift
]

# We can format these results like this to make something understandable:

r2 = lambda x:round(x,2)

# Here's a list-of-ist summary.
# ..    parsed-literal::
#
#       list(list(map(r2, row)) for row in expected)
#
# This structure shows following expected values for defect counts
#
# ..    parsed-literal::
#       [
#          [22.51, 20.99, 38.94, 11.56],
#          [22.99, 21.44, 39.77, 11.81],
#          [28.5, 26.57, 49.29, 14.63]
#       ]
#
# Each cell is based on a contribution of shift and type to the overall
# number of defects.
#
# Note the imporant difference from the expectation that the number of defects
# would be :math:`\frac{309}{12} = 25.75` in all cases. We're not asserting
# that shift and type of defect have no effect. We're asserting that the
# effects are independent of each other.
#
# For example, the different shifts may have different numbers of workers.
# It might be perfectly reasonable for one shift to produce more wafers
# and therefore more defects. Using actual shift totals to compute
# the probabilities reflects the idea that the observed counts will vary.

# Displaying the Contingency Table
# --------------------------------

# We can display the observed and expected
# in a single table. This involves a bit of restructuring the data
# to show defects and expected values side-by-side.

print("obs exp    "*4)
for s in range(3):
    pairs = '  '.join(
        f"{defects[s][t]:3d} {expected[s][t]:5.2f}" for t in range(4))
    print(f"{pairs}  {shift_total[s]:3d}")
footer = '        '.join(f"{type_total[t]:3d}" for t in range(4))
print(f"{footer}        {total:3d}")

# For each of the three shifts, we produced a row of data.
# Each row was pairs of observed and expected organized by defect
# type.
#
# The output looks like this:
#
# ..  parsed-literal::
#
#       obs exp    obs exp    obs exp    obs exp
#        15 22.51   21 20.99   45 38.94   13 11.56   94
#        26 22.99   31 21.44   34 39.77    5 11.81   96
#        33 28.50   17 26.57   49 49.29   20 14.63  119
#        74         69        128         38        309
#
# This shows the observed defects and the expected defects.
# It shows the shift totals and the defect type totals, also.
#
# In many practical applications, producing a text report like this
# isn't really optimal. It's often nicer to write a CSV file that
# can be reformatted for display. Using tools like Pandas xlsx writer
# can provide more useful output.
#
# Here's the CSV version of the output. It requires a function
# to properly flatten and interleave defects and expected values.

def flatten(defects, expected=None):
    for t in range(4):
        yield defects[t]
        if expected:
            yield expected[t]
        else:
            yield None

# This is similar in philosophy to the ``itertools.zip_longest()`` function.
# It interleaves values from defects and an optional second iterable.
# It can also be used to emit headers and footers; these situations don't
# have both iterables.

import csv

with open("contigency.csv", "w", newline="") as output:
    wtr=csv.writer(output)
    wtr.writerow(["shift"]+list(flatten(("A","B","C","D")))+["total"])
    wtr.writerow(["","obs","exp","obs","exp","obs","exp","obs","exp"])
    for s in range(3):
        row= [s]+list(flatten(defects[s],expected[s]))+[shift_total[s]]
        wtr.writerow(row)
    row= ["total"]+list(flatten(type_total))+[total]
    wtr.writerow(row)

# We've opened a writer and put out two lines of titles as a heading.
# The ``list(flatten(("A","B","C","D")))`` produces eight values by
# interleaving the four defect types and an equal number of ``None`` values.
#
# The body includes the interleaved defect counts and expected counts. Each
# row has a shift number as a header and a shift total as a summary.
#
# The total line uses ``list(flatten(type_total))`` to interleave the
# defect type totals with None values to create a footer line.
#
# Based on the totals, the third shift is expected to be more productive
# than the first two. Similarly, defect type "C" is expected to show up
# considerably more often than defect type "D".
#
# The question is "do the cell details reflect the overall summaries?"

# Applying the χ² test
# --------------------

# The final χ² value involves :math:`\sum_s \sum_t \frac{(E_{st}-d_{st})^2}{E_{st}}`
#
# We have three broad design patterns for workting with parallel nested structures:
#
# 1. Sum of sums. This involves a ``sum(map(sum, iterable))`` expression.
#    Since we have two structures that must be compared, this is really a bit
#    more complex than it appears. We need to compute the differences
#    before summing.
#
# 2. Use all combinations of index values.
#
# 3. Flatten both expected and actual and use a single sum.
#
# The second approach is how we produced the contingency table, above.
#
# We'll look at the third approach, also.
#
# Both will benefit from a handy lambda that allows us to compute the squared
# difference value between expected, ``e``, and observed, ``o``.

diff = lambda e,o: (e-o)**2/e

# We can use this lambda with all combinations of indices like this.

chi2 = sum(
    diff(expected[s][t], defects[s][t])
    for s in range(3)
    for t in range(4)
)

# We can also apply this lambda to two flattened sequences like this:

chi2 = sum(
    map(diff,
        (e for shift in expected for e in shift),
        (o for shift in defects for o in shift),
    )
)

# Either version gets us a χ² value, ``chi2``, of 19.18. There are six degrees
# of freedom in this model: 3-1=2 shifts times 4-1=3 types.

print(f"χ² = {chi2:.2f}, P = {cdf(chi2, 6):.5f}")

# The output looks like this:
#
# ..    parsed-literal::
#
#       χ² = 19.18, P = 0.00387
#
# The probability of this data being random is very low. There's something
# going on here that deserves further investigation. In formal terms,
# we must reject the null hypothesis.

# Functional Python Notes
# =======================

# Generally, each step has been defined by functional programming design
# patterns. We've accumulated totals, transformed them to probabilities,
# and then transformed the probabilities into expected values.
# We computed the χ² and compared this with the χ² cumulative distribution
# function to measure the randomness of the data.
#
# Each stage has been done with generator expressions and higher-order
# functions.
#
# In order to produce a printed report or CSV output file, we had to
# step back from purely functional programming. In these two cases,
# we used Python imperative programming techniques to structure
# the output in the intended format.
