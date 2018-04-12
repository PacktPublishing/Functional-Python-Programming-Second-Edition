#!/usr/bin/env python3
"""Functional Python Programming

Chapter 15, Example Set 4

typical URL.s

http://localhost:8080/anscombe/I?form=xml
http://localhost:8080/anscombe/II?form=json
http://localhost:8080/anscombe/III?form=csv
http://localhost:8080/anscombe/IV?form=html

"""
# pylint: disable=wrong-import-position,wrong-import-order,reimported

from Chapter03.ch03_ex5 import (
    series, head_map_filter, row_iter)

from typing import (
    NamedTuple, Callable, List, Tuple, Iterable, Dict, Any)

class Pair(NamedTuple):
    x: float
    y: float

RawPairIter = Iterable[Tuple[float, float]]

pairs: Callable[[RawPairIter], List[Pair]] \
     = lambda source: list(Pair(*row) for row in source)

def raw_data() -> Dict[str, List[Pair]]:
    """
    >>> with open("Anscombe.txt") as source:
    ...    data = tuple(head_map_filter(row_iter(source)))
    ...
    >>> data  # doctest: +ELLIPSIS
    ([10.0, 8.04, 10.0, 9.14, 10.0, 7.46, 8.0, 6.58], ...)
    >>> raw_data()['I']  # doctest: +ELLIPSIS
    [Pair(x=10.0, y=8.04), Pair(x=8.0, y=6.95), ...
    """
    with open("Anscombe.txt") as source:
        data = tuple(head_map_filter(row_iter(source)))
        mapping = {
            id_str: pairs(series(id_num, data))
            for id_num, id_str in enumerate(['I', 'II', 'III', 'IV'])
        }
    return mapping

def anscombe_filter(
        set_id: str, raw_data_map: Dict[str, List[Pair]]
    ) -> List[Pair]:
    """
    >>> anscombe_filter( "II", raw_data() )  # doctest: +ELLIPSIS
    [Pair(x=10.0, y=9.14), Pair(x=8.0, y=8.14), Pair(x=13.0, y=8.74), ...
    """
    return raw_data_map[set_id]

from typing import Callable, TypeVar, Any, cast

from functools import wraps
def to_bytes(function: Callable[..., str]) -> Callable[..., bytes]:
    @wraps(function)
    def decorated(*args, **kw):
        text = function(*args, **kw)
        return text.encode("utf-8")
    return cast(Callable[..., bytes], decorated)

import xml.etree.ElementTree as XML
def serialize_xml(series: str, data: List[Pair]) -> bytes:
    """
    >>> data = [Pair(2,3), Pair(5,7)]
    >>> serialize_xml( "test", data )
    b'<series name="test"><row><x>2</x><y>3</y></row><row><x>5</x><y>7</y></row></series>'
    """
    doc = XML.Element("series", name=series)
    for row in data:
        row_xml = XML.SubElement(doc, "row")
        x = XML.SubElement(row_xml, "x")
        x.text = str(row.x)
        y = XML.SubElement(row_xml, "y")
        y.text = str(row.y)
    return cast(bytes, XML.tostring(doc, encoding='utf-8'))

import string
data_page = string.Template("""\
<html>
<head><title>Series ${title}</title></head>
<body>
<h1>Series ${title}</h1>
<table>
<thead><tr><td>x</td><td>y</td></tr></thead>
<tbody>
${rows}
</tbody>
</table>
</body>
</html>
""")
@to_bytes
def serialize_html(series: str, data: List[Pair]) -> str:
    """
    >>> data = [Pair(2,3), Pair(5,7)]
    >>> serialize_html( "test", data ) #doctest: +ELLIPSIS
    b'<html>...<tr><td>2</td><td>3</td></tr>\\n<tr><td>5</td><td>7</td></tr>...
    """
    text = data_page.substitute(
        title=series,
        rows="\n".join(
            "<tr><td>{0.x}</td><td>{0.y}</td></tr>".format(row)
            for row in data)
        )
    return text

import json
@to_bytes
def serialize_json(series: str, data: List[Pair]) -> str:
    """
    >>> data = [Pair(2,3), Pair(5,7)]
    >>> serialize_json( "test", data )
    b'[{"x": 2, "y": 3}, {"x": 5, "y": 7}]'
    """
    obj = [dict(x=r.x, y=r.y) for r in data]
    text = json.dumps(obj, sort_keys=True)
    return text

import csv
import io

@to_bytes
def serialize_csv(series: str, data: List[Pair]) -> str:
    """
    >>> data = [Pair(2,3), Pair(5,7)]
    >>> serialize_csv("test", data)
    b'x,y\\r\\n2,3\\r\\n5,7\\r\\n'
    """
    buffer = io.StringIO()
    wtr = csv.DictWriter(buffer, Pair._fields)
    wtr.writeheader()
    wtr.writerows(r._asdict() for r in data)
    return buffer.getvalue()

Serializer = Callable[[str, List[Pair]], bytes]
serializers: Dict[str, Tuple[str, Serializer]]= {
    'xml': ('application/xml', serialize_xml),
    'html': ('text/html', serialize_html),
    'json': ('application/json', serialize_json),
    'csv': ('text/csv', serialize_csv),
}

def serialize(format: str, title: str, data: List[Pair]) -> Tuple[bytes, str]:
    """json/xml/csv/html serialization.

    >>> data = [Pair(2,3), Pair(5,7)]
    >>> serialize("json", "test", data)
    (b'[{"x": 2, "y": 3}, {"x": 5, "y": 7}]', 'application/json')
    """
    mime, function = serializers.get(
        format.lower(), ('text/html', serialize_html))
    return function(title, data), mime

import string

error_page = string.Template("""
<html>
<head><title>${title}</title></head>
<body>
<h1>Error</h1>
<p>${message}</p>
<pre><code>${traceback}</code></pre>
</body>
</html>
""")

import re
path_pat = re.compile(r"^/anscombe/(?P<dataset>.*?)/?$")

test_pattern = """
>>> m1= path_pat.match( "/anscombe/I" )
>>> m1.groupdict()
{'dataset': 'I'}
>>> m2= path_pat.match( "/anscombe/II/" )
>>> m2.groupdict()
{'dataset': 'II'}
>>> m3= path_pat.match( "/anscombe/" )
>>> m3.groupdict()
{'dataset': ''}
"""

from typing import Callable, List, Tuple, Iterable
from mypy_extensions import DefaultArg

SR_Func = Callable[[str, List[Tuple[str, str]], DefaultArg(Tuple)], None]

import traceback
import urllib.parse
def anscombe_app(environ: Dict, start_response: SR_Func) -> Iterable[bytes]:
    log = environ['wsgi.errors']
    try:
        match = path_pat.match(environ['PATH_INFO'])
        set_id = match.group('dataset').upper()
        query = urllib.parse.parse_qs(environ['QUERY_STRING'])
        print(environ['PATH_INFO'], environ['QUERY_STRING'],
              match.groupdict(), file=log)
        log.flush()

        dataset = anscombe_filter(set_id, raw_data())
        content_bytes, mime = serialize(query['form'][0], set_id, dataset)

        headers = [
            ('Content-Type', mime),
            ('Content-Length', str(len(content_bytes))),
        ]
        start_response("200 OK", headers)
        return [content_bytes]
    except Exception as e:  # pylint: disable=broad-except
        traceback.print_exc(file=log)
        tb = traceback.format_exc()
        content = error_page.substitute(
            title="Error", message=repr(e), traceback=tb)
        content_bytes = content.encode("utf-8")
        headers = [
            ('Content-Type', "text/html"),
            ('Content-Length', str(len(content_bytes))),
        ]
        start_response("404 NOT FOUND", headers)
        return [content_bytes]

__test__ = {
    "test_pattern": test_pattern,
}

def server_demo():
    from wsgiref.simple_server import make_server
    httpd = make_server('', 8080, anscombe_app)
    print("Serving HTTP on port 8080...")

    # Respond to requests until process is killed
    httpd.serve_forever()

def test():
    import doctest
    doctest.testmod(verbose=1)

if __name__ == "__main__":
    test()
    # server_demo()
