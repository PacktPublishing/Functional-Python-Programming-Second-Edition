#!/usr/bin/env python3
"""Functional Python Programming

Chapter 15, Example Set 1
"""
# pylint: disable=line-too-long,no-member
import http.client
import urllib.request
from contextlib import closing

def client_demo():
    with closing(
        http.client.HTTPConnection(
            "slott-softwarearchitect.blogspot.com", 80)) as server:
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-us",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10) AppleWebKit/600.1.25 (KHTML, like Gecko) Version/8.0 Safari/600.1.25",
        }
        server.request("GET", "/", headers=headers)
        response = server.getresponse()
        print(response.status, response.reason)
        body = response.read()
        print(body)
        with open("response.html", "wb") as result:
            result.write(body)

def urllib_demo():
    with urllib.request.urlopen(
        "http://slott-softwarearchitect.blogspot.com") as response:
        print(response.read())

def test():
    import doctest
    doctest.testmod(verbose=1)

if __name__ == "__main__":
    test()
    #client_demo()
    #urllib_demo()
