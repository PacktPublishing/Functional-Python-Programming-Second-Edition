"""
Stub for a few features of the PIL Image class.

To use this.

::

    export MYPYPATH=/path/to/your/stubs
    
The `stubs` directory name must be last. Replace `/path/to/your` with
the actual path to the download directory with the stubs.

NOTE.

This assumes RGB multi-band images. This is not true in general,
and the proper definition of a pixel should be something more along
the lines of ``Union[int, Tuple]``.
"""

from typing import *

class Image:
    def __init__(self): ...
    @property
    def size(self) -> Tuple[int, int]: ...
    def getpixel(self, coordinate: Tuple[int, int]) -> Tuple[int, int, int]: ...
    def putpixel(self, coordinate: Tuple[int, int], value: Tuple[int, int, int]): ...
    def copy(self) -> Image: ...
    def show(self): ...
    @staticmethod
    def open(filename: str) -> Image: ...
