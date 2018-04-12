#!/usr/bin/env python3
"""Functional Python Programming

Chapter 3, Example Set 2
"""

from decimal import Decimal
from typing import Text, Optional
def clean_decimal_1(text: Text) -> Optional[Decimal]:
    """
    Remove $ and , from a string, return a Decimal.

    >>> clean_decimal_1("$1,234.56")
    Decimal('1234.56')
    """
    if text is None:
        return None
    return Decimal(text.replace("$", "").replace(",", ""))

def replace(text: Text, a: Text, b: Text) -> Text:
    """Prefix function for str.replace(a,b)."""
    return text.replace(a, b)

def clean_decimal_2(text: Text) -> Optional[Decimal]:
    """
    Remove $ and , from a string, return a Decimal.

    >>> clean_decimal_2("$1,234.56")
    Decimal('1234.56')
    """
    if text is None:
        return None
    return Decimal(replace(replace(text, "$", ""), ",", ""))


def remove(text: Text, chars: Text) -> Text:
    """Remove all of the given chars from a string."""
    if chars:
        return remove(
            text.replace(chars[0], ""),
            chars[1:]
        )
    return text

def clean_decimal_3(text: Text) -> Optional[Decimal]:
    """
    Remove $ and , from a string, return a Decimal.

    >>> clean_decimal_3("$1,234.56")
    Decimal('1234.56')
    """
    if text is None:
        return None
    return Decimal(remove(text, "$,"))


def test():  # pylint: disable=missing-docstring
    import doctest
    doctest.testmod(verbose=2)

if __name__ == "__main__":
    test()
