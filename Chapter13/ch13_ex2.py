#!/usr/bin/env python3
"""Functional Python Programming

Chapter 13, Example Set 2
"""
# pylint: disable=unused-wildcard-import,wrong-import-position,unused-import

import re
p1 = re.compile(r"(some) pattern")
p2 = re.compile(r"a (different) pattern")

from typing import Optional, Match
def matcher(text: str) -> Optional[Match[str]]:
    patterns = [p1, p2]
    matching = (p.search(text) for p in patterns)
    try:
        good = next(filter(None, matching))
        return good
    except StopIteration:
        pass
    return None

test_matcher = '''
>>> text = "nothing"
>>> matcher(text)
>>> text = "this has some pattern in it"
>>> matcher(text)
<_sre.SRE_Match object; span=(9, 21), match='some pattern'>
'''

__test__ = {
    'test_matcher': test_matcher
}

def test():
    import doctest
    doctest.testmod(verbose=1)

if __name__ == "__main__":
    test()
