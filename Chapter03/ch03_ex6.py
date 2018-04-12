#!/usr/bin/env python3
"""Functional Python Programming

Chapter 3, Example Set 6
"""
# pylint: disable=line-too-long,wrong-import-position,reimported


# from collections import namedtuple
# Color = namedtuple("Color", ("red", "green", "blue", "name"))

from typing import NamedTuple
class Color(NamedTuple):
    """An RGB color."""
    red: int
    green: int
    blue: int
    name: str

example = '''GIMP Palette
Name: Small
Columns: 3
#
  0   0   0	Black
255 255 255	White
238  32  77	Red
28 172 120	Green
31 117 254	Blue
'''

import re
from typing import TextIO, Tuple, Iterator, List

def color_GPL_r(file_obj: TextIO) -> Iterator[Color]:
    """GPL Color Reader. Get body from the results of getting the header.

    Strictly recursive.

    >>> import io
    >>> data= io.StringIO("GIMP Palette\\nName: Crayola\\nColumns: 16\\n#\\n239 222 205	Almond\\n205 149 117	Antique Brass")
    >>> list( color_GPL_r(data))
    [Color(red=239, green=222, blue=205, name='Almond'), Color(red=205, green=149, blue=117, name='Antique Brass')]
    """
    header_pat = re.compile(r"GIMP Palette\nName:\s*(.*?)\nColumns:\s*(.*?)\n#\n", re.M)
    def read_head(file_obj: TextIO) -> Tuple[TextIO, str, str, str]:
        match = header_pat.match("".join(file_obj.readline() for _ in range(4)))
        return file_obj, match.group(1), match.group(2), file_obj.readline().rstrip()

    def read_tail(file_obj: TextIO, palette_name: str, columns: str, next_line: str) -> Iterator[Color]:
        if len(next_line) == 0: return
        r, g, b, *name = next_line.split()
        yield Color(int(r), int(g), int(b), " ".join(name))
        yield from read_tail(file_obj, palette_name, columns, file_obj.readline().rstrip())

    return read_tail(*read_head(file_obj))

def row_iter_gpl(file_obj: TextIO) -> Tuple[str, str, Iterator[List[str]]]:
    """GPL Color Reader. Get body from the results of getting the header.

    Uses a higher-level function in the form of a generator expression. Somewhat simpler.

    >>> import io
    >>> data= io.StringIO("GIMP Palette\\nName: Crayola\\nColumns: 16\\n#\\n239 222 205	Almond\\n205 149 117	Antique Brass")
    >>> name, columns, colors= row_iter_gpl(data)
    >>> name
    'Crayola'
    >>> list(colors)
    [['239', '222', '205', 'Almond'], ['205', '149', '117', 'Antique', 'Brass']]

    """
    header_pat = re.compile(r"GIMP Palette\nName:\s*(.*?)\nColumns:\s*(.*?)\n#\n", re.M)
    def read_head(file_obj: TextIO) -> Tuple[str, str, TextIO]:
        match = header_pat.match("".join(file_obj.readline() for _ in range(4)))
        return match.group(1), match.group(2), file_obj

    def read_tail(name: str, columns: str, file_obj: TextIO) -> Tuple[str, str, Iterator[List[str]]]:
        return name, columns, (next_line.split() for next_line in file_obj)

    return read_tail(*read_head(file_obj))

def color_GPL_g(file_obj: TextIO) -> Iterator[Color]:
    """GPL Color Reader. Generator function version which leverages
    the lower-level row_iter_gpl() function.

    >>> import io
    >>> data= io.StringIO("GIMP Palette\\nName: Crayola\\nColumns: 16\\n#\\n239 222 205	Almond\\n205 149 117	Antique Brass")
    >>> list( color_GPL_g(data))
    [Color(red=239, green=222, blue=205, name='Almond'), Color(red=205, green=149, blue=117, name='Antique Brass')]
    """
    # pylint: disable=unused-variable
    name, columns, row_iter = row_iter_gpl(file_obj)
    return (
        Color(int(r), int(g), int(b), " ".join(name))
        for r, g, b, *name in row_iter
        )

from typing import Iterator, Dict
def load_colors(row_iter_gpl: Tuple[str, str, Iterator[List[str]]]) -> Dict[str, Color]:
    """Load colors from the ``crayola.gpl`` file, building a mapping.

    >>> import io
    >>> source= io.StringIO(example)
    >>> colors= load_colors(row_iter_gpl(source))
    >>> [colors[k] for k in sorted(colors)]
    [Color(red=0, green=0, blue=0, name='Black'), Color(red=31, green=117, blue=254, name='Blue'), Color(red=28, green=172, blue=120, name='Green'), Color(red=238, green=32, blue=77, name='Red'), Color(red=255, green=255, blue=255, name='White')]
    """
    # pylint: disable=unused-variable
    name, columns, row_iter = row_iter_gpl
    colors = tuple(
        Color(int(r), int(g), int(b), " ".join(name))
        for r, g, b, *name in row_iter
    )
    #print( colors )
    mapping = dict((c.name, c) for c in colors)
    #print( mapping )
    return mapping

import bisect
from collections import Mapping
from typing import Iterable, Tuple, Any

class StaticMapping(Mapping):
    """
    >>> import io
    >>> c= StaticMapping( (c.name, c) for c in color_GPL_r(io.StringIO(example)) )
    >>> c.get("Black")
    Color(red=0, green=0, blue=0, name='Black')
    """
    def __init__(self, iterable: Iterable[Tuple[Any, Any]]) -> None:
        self._data = tuple(iterable)
        self._keys = tuple(sorted(key for key, _ in self._data))

    def __getitem__(self, key):
        ix = bisect.bisect_left(self._keys, key)
        if ix != len(self._keys) and self._keys[ix] == key:
            return self._data[ix][1]
        raise ValueError("{0!r} not found".format(key))
    def __iter__(self):
        return iter(self._keys)
    def __len__(self):
        return len(self._keys)

t1 = """
>>> import io
>>> tuple(color_GPL_r(io.StringIO(example)))
(Color(red=0, green=0, blue=0, name='Black'), Color(red=255, green=255, blue=255, name='White'), Color(red=238, green=32, blue=77, name='Red'), Color(red=28, green=172, blue=120, name='Green'), Color(red=31, green=117, blue=254, name='Blue'))
>>> tuple(color_GPL_g(io.StringIO(example)))
(Color(red=0, green=0, blue=0, name='Black'), Color(red=255, green=255, blue=255, name='White'), Color(red=238, green=32, blue=77, name='Red'), Color(red=28, green=172, blue=120, name='Green'), Color(red=31, green=117, blue=254, name='Blue'))
"""

t2 = """
>>> from typing import Tuple, Callable
>>> RGB = Tuple[int, int, int]
>>> red: Callable[[RGB], int] = lambda color: color[0]
>>> green: Callable[[RGB], int] = lambda color: color[1]
>>> blue: Callable[[RGB], int] = lambda color: color[2]
>>> almond = (239, 222, 205)
>>> red(almond)
239
"""

__test__ = {
    't1': t1,
    't2': t2
}
def test():
    import doctest
    doctest.testmod(verbose=1)

if __name__ == "__main__":
    test()
