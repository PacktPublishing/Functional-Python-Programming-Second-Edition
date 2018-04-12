"""
Stub for a few features of the bs4 BeautifulSoup class.

To use this.

::

    export MYPYPATH=/path/to/your/stubs
"""

from typing import *

class BeautifulSoup(Iterable):
    def __init__(self, source: bytes, parser: Optional[str]=None) -> None: ...
    
    html: BeautifulSoup
    body: BeautifulSoup
    table: BeautifulSoup
    children: BeautifulSoup
    text: str
    
    def __iter__(self) -> Iterator[BeautifulSoup]: ...
