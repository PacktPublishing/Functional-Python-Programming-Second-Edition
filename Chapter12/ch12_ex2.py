#!/usr/bin/env python3
"""Functional Python Programming

Chapter 12, Example Set 2
"""
# pylint: disable=reimported,wrong-import-position

import glob
import re
import ftplib
import gzip
import datetime
from collections import namedtuple
from typing import NamedTuple
import urllib.parse
import sys
import os
import time

# Some sample log lines for testing.

sample = """\
99.49.32.197 - - [01/Jun/2012:22:17:54 -0400] "GET /favicon.ico HTTP/1.1" 200 894 "-" "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.52 Safari/536.5"
66.249.71.25 - - [01/Jun/2012:22:17:55 -0400] "GET /book/python-2.6/html/p02/p02c10_adv_seq.html HTTP/1.1" 200 121825 "-" "Mediapartners-Google"
176.53.58.137 - - [01/Jun/2012:22:18:18 -0400] "GET /book/python-2.6/html/p04/p04c09_architecture.html HTTP/1.0" 200 193000 "http://www.itmaybeahack.com/book/python-2.6/html/p04/p04c09_architecture.html" "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 6.0 ; .NET CLR 2.0.50215; SL Commerce Client v1.0; Tablet PC 2.0"
176.53.58.137 - - [01/Jun/2012:22:18:20 -0400] "GET /p03/p03c04_extending.html HTTP/1.0" 404 331 "http://www.itmaybeahack.com/p03/p03c04_extending.html" "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 6.0 ; .NET CLR 2.0.50215; SL Commerce Client v1.0; Tablet PC 2.0"
176.53.58.137 - - [01/Jun/2012:22:18:20 -0400] "GET /p03c04_extending.html HTTP/1.0" 404 331 "http://www.itmaybeahack.com/p03c04_extending.html" "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 6.0 ; .NET CLR 2.0.50215; SL Commerce Client v1.0; Tablet PC 2.0"
137.111.13.200 - - [01/Jun/2012:22:18:32 -0400] "GET /homepage/books/nonprog/html/_static/doctools.js HTTP/1.1" 200 6618 "http://www.itmaybeahack.com/homepage/books/nonprog/html/p10_set_map/p10_c04_defaultdict.html" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_4) AppleWebKit/534.56.5 (KHTML, like Gecko) Version/5.1.6 Safari/534.56.5"
137.111.13.200 - - [01/Jun/2012:22:18:28 -0400] "GET /homepage/books/nonprog/html/p10_set_map/p10_c04_defaultdict.html HTTP/1.1" 200 29101 "http://www.google.com.au/url?sa=t&rct=j&q=defaultdict%20list&source=web&cd=3&ved=0CFoQFjAC&url=http%3A%2F%2Fwww.itmaybeahack.com%2Fhomepage%2Fbooks%2Fnonprog%2Fhtml%2Fp10_set_map%2Fp10_c04_defaultdict.html&ei=z3fJT8-nHce3iQfo6ZnNBg&usg=AFQjCNFckv6gmMcbvtMFDOyjAcVlQDiYvA&sig2=i12vAm4yVbB0QyMgUZmEgg" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_4) AppleWebKit/534.56.5 (KHTML, like Gecko) Version/5.1.6 Safari/534.56.5"
137.111.13.200 - - [01/Jun/2012:22:18:33 -0400] "GET /homepage/books/nonprog/html/_static/pygments.css HTTP/1.1" 200 3224 "http://www.itmaybeahack.com/homepage/books/nonprog/html/p10_set_map/p10_c04_defaultdict.html" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_4) AppleWebKit/534.56.5 (KHTML, like Gecko) Version/5.1.6 Safari/534.56.5"
"""

# Stage I: Lines of source.

from typing import Iterator
def local_gzip(pattern: str) -> Iterator[Iterator[str]]:
    """
    Local downloads of gzip log files.
    Yields a sequence of iterators over lines, one for each file.
    """
    zip_logs = glob.glob(pattern)
    print("Analyzing", zip_logs)
    print()
    sys.stdout.flush()
    for zip_file in zip_logs:
        with gzip.open(zip_file, "rb") as log:
            yield (line.decode('us-ascii').rstrip() for line in log)

from typing import Iterator
def remote_source(**credentials) -> Iterator[Iterator[str]]:
    """A2 Hosting FTP URL.
    Uses to local_gzip() to yield a sequence of iterators, one for each file.
    """
    with ftplib.FTP("ftp.itmaybeahack.com", **credentials) as ftp:
        try:
            ftp.login()
        except ftplib.error_perm as e:
            if e.args[0].startswith("530"):
                pass
            else:
                raise
        ftp.cwd("logs")
        for name in ftp.nlst():
            if name.startswith("."):
                continue
            command = "RETR {0}".format(name)
            ftp.retrbinary(command, open(name, 'wb').write)
        ftp.quit()
    yield from local_gzip("ftp.itmaybeahack.com.*.gz")
    #for file_iter in local_gzip("ftp.itmaybeahack.com.*.gz"):
    #    yield file_iter

from typing import Iterator
def local_gzip2(pattern: str) -> Iterator[Iterator[str]]:
    def line_iter(zip_file: str) -> Iterator[str]:
        """Opens and returns iterator over cleaned lines."""
        log = gzip.open(zip_file, "rb")
        return (line.decode('us-ascii').rstrip() for line in log)
    return map(line_iter, glob.glob(pattern))

test_local_gzip = """
>>> file_iter = local_gzip( "example.log.gz" )
>>> data= tuple(next(file_iter))
Analyzing ['example.log.gz']
<BLANKLINE>
>>> [len(line) for line in data]
[187, 144, 317, 266, 258, 335, 559, 336]
>>> more= tuple(next(file_iter)) # doctest: +ELLIPSIS
Traceback (most recent call last):
...
StopIteration
"""

test_local_gzip2 = """
>>> for log in local_gzip2("example.log.gz"):
...    print( [len(line) for line in log] )
[187, 144, 317, 266, 258, 335, 559, 336]
"""

def sample_data():
    """Read lines for unit tests, below."""
    yield sample.splitlines()

test_sample_data = """
>>> for log in sample_data():
...    print( [len(line) for line in log] )
[187, 144, 317, 266, 258, 335, 559, 336]
"""


# Stage II: Access objects

format_pat = re.compile(
    r"(?P<host>[\d\.]+)\s+"
    r"(?P<identity>\S+)\s+"
    r"(?P<user>\S+)\s+"
    r"\[(?P<time>.+?)\]\s+"
    r'"(?P<request>.+?)"\s+'
    r"(?P<status>\d+)\s+"
    r"(?P<bytes>\S+)\s+"
    r'"(?P<referer>.*?)"\s+' # [SIC]
    r'"(?P<user_agent>.+?)"\s*'
)

from typing import NamedTuple
class Access(NamedTuple):
    # pylint: disable=too-few-public-methods
    """A line from the log, parsed into strings."""
    host: str
    identity: str
    user: str
    time: str
    request: str
    status: str
    bytes: str
    referer: str
    user_agent: str

from typing import Iterator
def access_iter(source_iter: Iterator[Iterator[str]]) -> Iterator[Access]:
    """
    Yields single sequence of Access objects from
    a sequence of iterators created by local_gzip() or remote_source()
    """
    for log in source_iter:
        for line in log:
            match = format_pat.match(line)
            if match:
                yield Access(**match.groupdict())

from typing import Iterator, Optional
def access_iter2(source_iter: Iterator[Iterator[str]]) -> Iterator[Access]:
    """
    Yields single sequence of Access objects from
    a sequence of iterators created by local_gzip() or remote_source()
    """
    def access_builder(line: str) -> Optional[Access]:
        """Conditionally creates Access object if the line matches."""
        match = format_pat.match(line)
        if match:
            return Access(**match.groupdict())
        return None
    return filter(
        None,
        map(
            access_builder,
            (line for log in source_iter for line in log)
        )
    )

test_access_iter = """
>>> data = list( access_iter( sample_data() ) )
>>> len(data)
8
>>> data[0]
Access(host='99.49.32.197', identity='-', user='-', time='01/Jun/2012:22:17:54 -0400', request='GET /favicon.ico HTTP/1.1', status='200', bytes='894', referer='-', user_agent='Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.52 Safari/536.5')
>>> data[-1]
Access(host='137.111.13.200', identity='-', user='-', time='01/Jun/2012:22:18:33 -0400', request='GET /homepage/books/nonprog/html/_static/pygments.css HTTP/1.1', status='200', bytes='3224', referer='http://www.itmaybeahack.com/homepage/books/nonprog/html/p10_set_map/p10_c04_defaultdict.html', user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_4) AppleWebKit/534.56.5 (KHTML, like Gecko) Version/5.1.6 Safari/534.56.5')
"""

test_access_iter2 = """
>>> data = list( access_iter2( sample_data() ) )
>>> len(data)
8
>>> data[0]
Access(host='99.49.32.197', identity='-', user='-', time='01/Jun/2012:22:17:54 -0400', request='GET /favicon.ico HTTP/1.1', status='200', bytes='894', referer='-', user_agent='Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.52 Safari/536.5')
>>> data[-1]
Access(host='137.111.13.200', identity='-', user='-', time='01/Jun/2012:22:18:33 -0400', request='GET /homepage/books/nonprog/html/_static/pygments.css HTTP/1.1', status='200', bytes='3224', referer='http://www.itmaybeahack.com/homepage/books/nonprog/html/p10_set_map/p10_c04_defaultdict.html', user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_4) AppleWebKit/534.56.5 (KHTML, like Gecko) Version/5.1.6 Safari/534.56.5')
"""


# Stage III. Access Details objects

# AccessDetails = namedtuple(
#    'AccessDetails',
#    ['access', 'time', 'method', 'url', 'protocol', 'referrer', 'agent']
# )

# AgentDetails = namedtuple(
#    'AgentDetails',
#    ['product', 'system', 'platform_details_extensions']
# )

from typing import NamedTuple, Optional
import datetime
import urllib.parse

class AgentDetails(NamedTuple):
    product: str
    system: str
    platform_details_extensions: str

class AccessDetails(NamedTuple):
    access: Access
    time: datetime.datetime
    method: str
    url: urllib.parse.ParseResult
    protocol: str
    referrer: urllib.parse.ParseResult
    agent: Optional[AgentDetails]

from typing import Tuple
def parse_request(request: str) -> Tuple[str, str, str]:
    words = request.split()
    return words[0], ' '.join(words[1:-1]), words[-1]

import datetime
def parse_time(ts: str) -> datetime.datetime:
    return datetime.datetime.strptime(ts, "%d/%b/%Y:%H:%M:%S %z")

agent_pat = re.compile(
    r"(?P<product>\S*?)\s+"
    r"\((?P<system>.*?)\)\s*"
    r"(?P<platform_details_extensions>.*)"
)

from typing import Optional
def parse_agent(user_agent: str) -> Optional[AgentDetails]:
    agent_match = agent_pat.match(user_agent)
    if agent_match:
        return AgentDetails(**agent_match.groupdict())
    return None

from typing import Iterable, Iterator
def access_detail_iter(access_iter: Iterable[Access]) -> Iterator[AccessDetails]:
    """Yields AccessDetails wrapped around the original Access objects."""
    for access in access_iter:
        try:
            meth, uri, protocol = parse_request(access.request)
            yield AccessDetails(
                access=access,
                time=parse_time(access.time),
                method=meth,
                url=urllib.parse.urlparse(uri),
                protocol=protocol,
                referrer=urllib.parse.urlparse(access.referer),
                agent=parse_agent(access.user_agent)
            )
        except ValueError as e:
            print(e, repr(access))

from typing import Iterable, Iterator
def access_detail_iter2(access_iter: Iterable[Access]) -> Iterator[AccessDetails]:
    def access_detail_builder(access: Access) -> Optional[AccessDetails]:
        try:
            meth, uri, protocol = parse_request(access.request)
            return AccessDetails(
                access=access,
                time=parse_time(access.time),
                method=meth,
                url=urllib.parse.urlparse(uri),
                protocol=protocol,
                referrer=urllib.parse.urlparse(access.referer),
                agent=parse_agent(access.user_agent)
            )
        except ValueError as e:
            print(e, repr(access))
        return None
    return filter(None, map(access_detail_builder, access_iter))

test_access_detail_iter = """
>>> data= list( access_detail_iter(access_iter( sample_data())))
>>> len(data)
8
>>> data[0]
AccessDetails(access=Access(host='99.49.32.197', identity='-', user='-', time='01/Jun/2012:22:17:54 -0400', request='GET /favicon.ico HTTP/1.1', status='200', bytes='894', referer='-', user_agent='Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.52 Safari/536.5'), time=datetime.datetime(2012, 6, 1, 22, 17, 54, tzinfo=datetime.timezone(datetime.timedelta(-1, 72000))), method='GET', url=ParseResult(scheme='', netloc='', path='/favicon.ico', params='', query='', fragment=''), protocol='HTTP/1.1', referrer=ParseResult(scheme='', netloc='', path='-', params='', query='', fragment=''), agent=AgentDetails(product='Mozilla/5.0', system='Windows NT 6.0', platform_details_extensions='AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.52 Safari/536.5'))
>>> data[-1]
AccessDetails(access=Access(host='137.111.13.200', identity='-', user='-', time='01/Jun/2012:22:18:33 -0400', request='GET /homepage/books/nonprog/html/_static/pygments.css HTTP/1.1', status='200', bytes='3224', referer='http://www.itmaybeahack.com/homepage/books/nonprog/html/p10_set_map/p10_c04_defaultdict.html', user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_4) AppleWebKit/534.56.5 (KHTML, like Gecko) Version/5.1.6 Safari/534.56.5'), time=datetime.datetime(2012, 6, 1, 22, 18, 33, tzinfo=datetime.timezone(datetime.timedelta(-1, 72000))), method='GET', url=ParseResult(scheme='', netloc='', path='/homepage/books/nonprog/html/_static/pygments.css', params='', query='', fragment=''), protocol='HTTP/1.1', referrer=ParseResult(scheme='http', netloc='www.itmaybeahack.com', path='/homepage/books/nonprog/html/p10_set_map/p10_c04_defaultdict.html', params='', query='', fragment=''), agent=AgentDetails(product='Mozilla/5.0', system='Macintosh; Intel Mac OS X 10_7_4', platform_details_extensions='AppleWebKit/534.56.5 (KHTML, like Gecko) Version/5.1.6 Safari/534.56.5'))
"""

test_access_detail_iter2 = """
>>> data= list( access_detail_iter2(access_iter( sample_data())))
>>> len(data)
8
>>> data[0]
AccessDetails(access=Access(host='99.49.32.197', identity='-', user='-', time='01/Jun/2012:22:17:54 -0400', request='GET /favicon.ico HTTP/1.1', status='200', bytes='894', referer='-', user_agent='Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.52 Safari/536.5'), time=datetime.datetime(2012, 6, 1, 22, 17, 54, tzinfo=datetime.timezone(datetime.timedelta(-1, 72000))), method='GET', url=ParseResult(scheme='', netloc='', path='/favicon.ico', params='', query='', fragment=''), protocol='HTTP/1.1', referrer=ParseResult(scheme='', netloc='', path='-', params='', query='', fragment=''), agent=AgentDetails(product='Mozilla/5.0', system='Windows NT 6.0', platform_details_extensions='AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.52 Safari/536.5'))
>>> data[-1]
AccessDetails(access=Access(host='137.111.13.200', identity='-', user='-', time='01/Jun/2012:22:18:33 -0400', request='GET /homepage/books/nonprog/html/_static/pygments.css HTTP/1.1', status='200', bytes='3224', referer='http://www.itmaybeahack.com/homepage/books/nonprog/html/p10_set_map/p10_c04_defaultdict.html', user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_4) AppleWebKit/534.56.5 (KHTML, like Gecko) Version/5.1.6 Safari/534.56.5'), time=datetime.datetime(2012, 6, 1, 22, 18, 33, tzinfo=datetime.timezone(datetime.timedelta(-1, 72000))), method='GET', url=ParseResult(scheme='', netloc='', path='/homepage/books/nonprog/html/_static/pygments.css', params='', query='', fragment=''), protocol='HTTP/1.1', referrer=ParseResult(scheme='http', netloc='www.itmaybeahack.com', path='/homepage/books/nonprog/html/p10_set_map/p10_c04_defaultdict.html', params='', query='', fragment=''), agent=AgentDetails(product='Mozilla/5.0', system='Macintosh; Intel Mac OS X 10_7_4', platform_details_extensions='AppleWebKit/534.56.5 (KHTML, like Gecko) Version/5.1.6 Safari/534.56.5'))
"""

# Stage IV: Reduce clutter

from typing import Iterable, Iterator
def path_filter(
        access_details_iter: Iterable[AccessDetails]
    ) -> Iterable[AccessDetails]:
    name_exclude = {
        'favicon.ico', 'robots.txt', 'index.php', 'humans.txt',
        'a2test', 'ping',
        'dompdf.php', 'crossdomain.xml',
        '_images', 'search.html', 'genindex.html',
        'searchindex.js', 'modindex.html', 'py-modindex.html',
    }
    ext_exclude = {
        '.png', '.js', '.css',
    }
    for detail in access_details_iter:
        path = detail.url.path.split('/')
        if not any(path):
            continue
        if any(p in name_exclude for p in path):
            continue
        final = path[-1]
        if any(final.endswith(ext) for ext in ext_exclude):
            continue
        yield detail

from typing import Iterable, Iterator
def path_filter2(
        access_details_iter: Iterable[AccessDetails]
    ) -> Iterable[AccessDetails]:
    def non_empty_path(detail: AccessDetails) -> bool:
        path = detail.url.path.split('/')
        return any(path)
    def non_excluded_names(detail: AccessDetails) -> bool:
        "Exclude by name; include names not in a list."
        name_exclude = {
            'favicon.ico', 'robots.txt', 'index.php', 'humans.txt',
            'a2test', 'ping',
            'dompdf.php', 'crossdomain.xml',
            '_images', 'search.html', 'genindex.html',
            'searchindex.js', 'modindex.html', 'py-modindex.html',
        }
        path = detail.url.path.split('/')
        return not any(p in name_exclude for p in path)
    def non_excluded_ext(detail: AccessDetails) -> bool:
        "Exclude by extension; include names not in a list."
        ext_exclude = {
            '.png', '.js', '.css',
        }
        path = detail.url.path.split('/')
        final = path[-1]
        return not any(final.endswith(ext) for ext in ext_exclude)
    ne = filter(non_empty_path, access_details_iter)
    nx_name = filter(non_excluded_names, ne)
    nx_ext = filter(non_excluded_ext, nx_name)
    return nx_ext
    # Yet another variation:
    # return filter( non_excluded_ext,
    #              filter( non_excluded_names,
    #                     filter( non_empty_path, access_details_iter ) ) )

test_path_filter = """
>>> data= list( path_filter( access_detail_iter(access_iter( sample_data()))) )
>>> len(data)
5
>>> data[0]
AccessDetails(access=Access(host='66.249.71.25', identity='-', user='-', time='01/Jun/2012:22:17:55 -0400', request='GET /book/python-2.6/html/p02/p02c10_adv_seq.html HTTP/1.1', status='200', bytes='121825', referer='-', user_agent='Mediapartners-Google'), time=datetime.datetime(2012, 6, 1, 22, 17, 55, tzinfo=datetime.timezone(datetime.timedelta(-1, 72000))), method='GET', url=ParseResult(scheme='', netloc='', path='/book/python-2.6/html/p02/p02c10_adv_seq.html', params='', query='', fragment=''), protocol='HTTP/1.1', referrer=ParseResult(scheme='', netloc='', path='-', params='', query='', fragment=''), agent=None)
>>> data[-1]
AccessDetails(access=Access(host='137.111.13.200', identity='-', user='-', time='01/Jun/2012:22:18:28 -0400', request='GET /homepage/books/nonprog/html/p10_set_map/p10_c04_defaultdict.html HTTP/1.1', status='200', bytes='29101', referer='http://www.google.com.au/url?sa=t&rct=j&q=defaultdict%20list&source=web&cd=3&ved=0CFoQFjAC&url=http%3A%2F%2Fwww.itmaybeahack.com%2Fhomepage%2Fbooks%2Fnonprog%2Fhtml%2Fp10_set_map%2Fp10_c04_defaultdict.html&ei=z3fJT8-nHce3iQfo6ZnNBg&usg=AFQjCNFckv6gmMcbvtMFDOyjAcVlQDiYvA&sig2=i12vAm4yVbB0QyMgUZmEgg', user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_4) AppleWebKit/534.56.5 (KHTML, like Gecko) Version/5.1.6 Safari/534.56.5'), time=datetime.datetime(2012, 6, 1, 22, 18, 28, tzinfo=datetime.timezone(datetime.timedelta(-1, 72000))), method='GET', url=ParseResult(scheme='', netloc='', path='/homepage/books/nonprog/html/p10_set_map/p10_c04_defaultdict.html', params='', query='', fragment=''), protocol='HTTP/1.1', referrer=ParseResult(scheme='http', netloc='www.google.com.au', path='/url', params='', query='sa=t&rct=j&q=defaultdict%20list&source=web&cd=3&ved=0CFoQFjAC&url=http%3A%2F%2Fwww.itmaybeahack.com%2Fhomepage%2Fbooks%2Fnonprog%2Fhtml%2Fp10_set_map%2Fp10_c04_defaultdict.html&ei=z3fJT8-nHce3iQfo6ZnNBg&usg=AFQjCNFckv6gmMcbvtMFDOyjAcVlQDiYvA&sig2=i12vAm4yVbB0QyMgUZmEgg', fragment=''), agent=AgentDetails(product='Mozilla/5.0', system='Macintosh; Intel Mac OS X 10_7_4', platform_details_extensions='AppleWebKit/534.56.5 (KHTML, like Gecko) Version/5.1.6 Safari/534.56.5'))
"""

test_path_filter2 = """
>>> data= list( path_filter2( access_detail_iter(access_iter( sample_data()))) )
>>> len(data)
5
>>> data[0]
AccessDetails(access=Access(host='66.249.71.25', identity='-', user='-', time='01/Jun/2012:22:17:55 -0400', request='GET /book/python-2.6/html/p02/p02c10_adv_seq.html HTTP/1.1', status='200', bytes='121825', referer='-', user_agent='Mediapartners-Google'), time=datetime.datetime(2012, 6, 1, 22, 17, 55, tzinfo=datetime.timezone(datetime.timedelta(-1, 72000))), method='GET', url=ParseResult(scheme='', netloc='', path='/book/python-2.6/html/p02/p02c10_adv_seq.html', params='', query='', fragment=''), protocol='HTTP/1.1', referrer=ParseResult(scheme='', netloc='', path='-', params='', query='', fragment=''), agent=None)
>>> data[-1]
AccessDetails(access=Access(host='137.111.13.200', identity='-', user='-', time='01/Jun/2012:22:18:28 -0400', request='GET /homepage/books/nonprog/html/p10_set_map/p10_c04_defaultdict.html HTTP/1.1', status='200', bytes='29101', referer='http://www.google.com.au/url?sa=t&rct=j&q=defaultdict%20list&source=web&cd=3&ved=0CFoQFjAC&url=http%3A%2F%2Fwww.itmaybeahack.com%2Fhomepage%2Fbooks%2Fnonprog%2Fhtml%2Fp10_set_map%2Fp10_c04_defaultdict.html&ei=z3fJT8-nHce3iQfo6ZnNBg&usg=AFQjCNFckv6gmMcbvtMFDOyjAcVlQDiYvA&sig2=i12vAm4yVbB0QyMgUZmEgg', user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_4) AppleWebKit/534.56.5 (KHTML, like Gecko) Version/5.1.6 Safari/534.56.5'), time=datetime.datetime(2012, 6, 1, 22, 18, 28, tzinfo=datetime.timezone(datetime.timedelta(-1, 72000))), method='GET', url=ParseResult(scheme='', netloc='', path='/homepage/books/nonprog/html/p10_set_map/p10_c04_defaultdict.html', params='', query='', fragment=''), protocol='HTTP/1.1', referrer=ParseResult(scheme='http', netloc='www.google.com.au', path='/url', params='', query='sa=t&rct=j&q=defaultdict%20list&source=web&cd=3&ved=0CFoQFjAC&url=http%3A%2F%2Fwww.itmaybeahack.com%2Fhomepage%2Fbooks%2Fnonprog%2Fhtml%2Fp10_set_map%2Fp10_c04_defaultdict.html&ei=z3fJT8-nHce3iQfo6ZnNBg&usg=AFQjCNFckv6gmMcbvtMFDOyjAcVlQDiYvA&sig2=i12vAm4yVbB0QyMgUZmEgg', fragment=''), agent=AgentDetails(product='Mozilla/5.0', system='Macintosh; Intel Mac OS X 10_7_4', platform_details_extensions='AppleWebKit/534.56.5 (KHTML, like Gecko) Version/5.1.6 Safari/534.56.5'))
"""

from typing import Iterable, Iterator
def book_filter(access_details_iter: Iterable[AccessDetails]) -> Iterator[AccessDetails]:
    def book_in_path(detail: AccessDetails) -> bool:
        path = tuple(l for l in detail.url.path.split('/') if l)
        return path[0] == 'book' and len(path) > 1
    return filter(book_in_path, access_details_iter)

from typing import Iterable, Iterator
def book_filter_opt(access_details_iter: Iterable[AccessDetails]) -> Iterator[AccessDetails]:
    """Creates a sequence of AccessDetails information from the '/book' path."""
    for detail in access_details_iter:
        path = tuple(l for l in detail.url.path.split('/') if l)
        if path[0] == 'book' and len(path) > 1:
            yield detail

from typing import Iterable, Iterator, Dict
from collections import Counter
def reduce_book_total(access_details_iter: Iterable[AccessDetails]) -> Dict[str, int]:
    counts: Dict[str, int] = Counter()
    for detail in access_details_iter:
        counts[detail.url.path] += 1
    return counts

test_book_filter = """
>>> details= path_filter( access_detail_iter(access_iter( sample_data())))
>>> data = book_filter( details )
>>> list( (d.url.path for d in data) )
['/book/python-2.6/html/p02/p02c10_adv_seq.html', '/book/python-2.6/html/p04/p04c09_architecture.html']
"""

test_book_filter_opt = """
>>> details= path_filter( access_detail_iter(access_iter( sample_data())))
>>> data = book_filter_opt( details )
>>> list( (d.url.path for d in data) )
['/book/python-2.6/html/p02/p02c10_adv_seq.html', '/book/python-2.6/html/p04/p04c09_architecture.html']
"""

test_book_count = """
>>> data = book_filter( path_filter( access_detail_iter(access_iter( sample_data()))) )
>>> totals = reduce_book_total( data )
>>> [(k,totals[k]) for k in sorted(totals.keys())]
[('/book/python-2.6/html/p02/p02c10_adv_seq.html', 1), ('/book/python-2.6/html/p04/p04c09_architecture.html', 1)]
"""

__test__ = {
    "Stage I: test_local_gzip": test_local_gzip,
    "Stage I: test_local_gzip2": test_local_gzip2,
    "Stage I: test_sample_data": test_sample_data,

    "Stage II: test_access_iter": test_access_iter,
    "Stage II: test_access_iter2": test_access_iter2,

    "Stage III: test_access_detail_iter": test_access_detail_iter,
    "Stage III: test_access_detail_iter2": test_access_detail_iter2,

    "Stage IV: test_path_filter": test_path_filter,
    "Stage IV: test_path_filter2": test_path_filter2,

    "test_book_filter": test_book_filter,
    "test_book_filter_opt": test_book_filter_opt,
    "test_book_count": test_book_count,
}

def test(*args, **kw):
    import doctest
    doctest.testmod(*args, **kw)

def analysis(filename: str) -> Dict[str, int]:
    """Count book chapters in a given file"""
    details = path_filter(
        access_detail_iter(
            access_iter(
                local_gzip(filename))))
    books = book_filter(details)
    totals = reduce_book_total(books)
    return totals

def demo_mp(pool_size=None):
    """6 large files, 5 small files.
    Actual time 69.8 sec with pool of 4 or more workers.
    """
    import multiprocessing
    root = "/Users/slott/Documents/Work/ItMayBeAHack/"

    start = time.perf_counter()

    pattern = root+"*itmaybeahack.com*.gz"
    pool_size = multiprocessing.cpu_count() if pool_size is None else pool_size
    combined = Counter()
    with multiprocessing.Pool(pool_size) as workers:
        for result in workers.imap_unordered(analysis, glob.glob(pattern)):
            combined.update(result)

    end = time.perf_counter()
    print(combined)
    print("time {0:.1f}, pool size {1:d}".format(end-start, pool_size))

def demo_mp_async(pool_size=None):
    """6 large files, 5 small files.
    Actual time 69.8 sec with pool of 4 or more workers.
    """
    import multiprocessing
    root = "/Users/slott/Documents/Work/ItMayBeAHack/"

    start = time.perf_counter()

    pattern = root+"*itmaybeahack.com*.gz"
    combined = Counter()
    pool_size = multiprocessing.cpu_count() if pool_size is None else pool_size
    with multiprocessing.Pool(pool_size) as workers:
        results = workers.map_async(analysis, glob.glob(pattern))
            # , callback=combined.update )
        data = results.get()
        for c in data:
            combined.update(c)

    end = time.perf_counter()
    print(combined)
    print("time {0:.1f}, pool size {1:d}".format(end-start, pool_size))

def demo_cf_threads():
    import concurrent.futures
    root = "/Users/slott/Documents/Work/ItMayBeAHack/"

    start = time.perf_counter()

    pool_size = 4
    pattern = root+"*itmaybeahack.com*.gz"
    combined = Counter()
    with concurrent.futures.ThreadPoolExecutor(max_workers=pool_size) as workers:
        for result in workers.map(analysis, glob.glob(pattern)):
            combined.update(result)

    end = time.perf_counter()
    print(combined)
    print("time {0:.1f}, pool size {1:d}".format(end-start, pool_size))

def demo_cf_procs():
    import concurrent.futures
    root = "/Users/slott/Documents/Work/ItMayBeAHack/"

    start = time.perf_counter()

    pool_size = 4
    pattern = root+"*itmaybeahack.com*.gz"
    combined = Counter()
    with concurrent.futures.ProcessPoolExecutor(max_workers=pool_size) as workers:
        for result in workers.map(analysis, glob.glob(pattern)):
            combined.update(result)

    end = time.perf_counter()
    print(combined)
    print("time {0:.1f}, pool size {1:d}".format(end-start, pool_size))

def benchmark():
    """
    6 large files, 5 small files.
    Actual time 26.5 sec for median file.
    Predicted 138.3 seconds total.
    """
    snd = lambda x: x[1]
    root = "/Users/slott/Documents/Work/ItMayBeAHack/"
    pattern = root+"*itmaybeahack.com*.gz"
    median_file = root+"itmaybeahack.com.bkup-May-2012.gz"

    start = time.perf_counter()
    analysis(median_file)
    end = time.perf_counter()
    print("size {0:,d} time {1:.1f}".format(os.path.getsize(median_file), end-start))

def estimates(rate=None):
    root = "/Users/slott/Documents/Work/ItMayBeAHack/"
    pattern = root+"*itmaybeahack.com*.gz"
    if rate is None:
        median_file = root+"itmaybeahack.com.bkup-May-2012.gz"
        median_size = os.path.getsize(median_file)
        median_time = 26
        rate = median_time/median_size
    t = 0
    for name in glob.glob(pattern):
        sz = os.path.getsize(name)
        print("name {0:s} size {1:,d} time {2:.1f}".format(name, sz, sz*rate))
        t += sz
    print("total {0:,d} time {1:.1f}".format(t, t*rate))

if __name__ == "__main__":
    with gzip.open("example.log.gz", 'wb') as example:
        example.write(sample.encode("us-ascii"))
    test(verbose=1)
    #benchmark()
    #estimates()
    #demo_mp()
    #demo_mp_async()
    #demo_cf_threads() # time 168.0, pool size 4
    #demo_cf_procs() # time 68.0, pool size 4
