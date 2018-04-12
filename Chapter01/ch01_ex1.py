#!/usr/bin/env python3
"""Functional Python Programming

Chapter 1, Example Set 1
"""

def sum_numeric():
    """Purely numeric.

    >>> sum_numeric()
    23
    """
    s = 0
    for n in range(1, 10):
        if n % 3 == 0 or n % 5 == 0:
            s += n
    print(s)

def sum_object_light():
    """Some Object Features.

    >>> sum_object_light()
    23
    """
    m = list()
    for n in range(1, 10):
        if n % 3 == 0 or n % 5 == 0:
            m.append(n)
    print(sum(m))

class Summable_List(list):
    def sum(self):
        s = 0
        for v in self:
            s += v
        return s

def sum_full_oo():
    """Full-on OO.

    >>> sum_full_oo()
    23
    """
    m = Summable_List()
    for n in range(1, 10):
        if n % 3 == 0 or n % 5 == 0:
            m.append(n)
    print(m.sum())

def foldr(seq, op, init):
    """Recursive sum.

    >>> foldr( [2,3,5,7], lambda x,y: x+y, 0 )
    17
    """
    if len(seq) == 0:
        return init
    return op(seq[0], sum(seq[1:]))

def until(n, filter_func, v):
    """Build a list: list( filter( filter_func, range(n) ) )

    >>> list( filter( lambda x: x%3==0 or x%5==0, range(10) ) )
    [0, 3, 5, 6, 9]
    >>> until(10, lambda x: x%3==0 or x%5==0, 0)
    [0, 3, 5, 6, 9]
    """
    if v == n:
        return []
    if filter_func(v):
        return [v] + until(n, filter_func, v+1)
    else:
        return until(n, filter_func, v+1)

def sum_functional():
    """
    >>> sum_functional()
    23
    """
    mult_3_5 = lambda x: x%3 == 0 or x%5 == 0
    add = lambda x, y: x+y
    return foldr(until(10, mult_3_5, 0), add, 0)

def sum_hybrid():
    """Hybrid Function.

    >>> sum_hybrid()
    23
    """
    print(sum(n for n in range(1, 10) if n%3 == 0 or n%5 == 0))

def folding():
    """Performance differences from folding.

    >>> ((([]+[1])+[2])+[3])+[4]
    [1, 2, 3, 4]
    >>> []+([1]+([2]+([3]+[4])))
    [1, 2, 3, 4]
    """
    print("foldl", timeit.timeit("((([]+[1])+[2])+[3])+[4]"))
    print("foldr", timeit.timeit("[]+([1]+([2]+([3]+[4])))"))

demo_1 = """
>>> def sumr(seq): 
...     if len(seq) == 0: return 0 
...     return seq[0] + sumr(seq[1:])
>>> sumr([7, 11])
18
>>> sumr([11])
11
>>> sumr([])
0
"""

__test__ = {
    'demo_1': demo_1
}

def test():
    import doctest
    doctest.testmod(verbose=1)

if __name__ == "__main__":
    test()
    # import timeit
    # folding()
