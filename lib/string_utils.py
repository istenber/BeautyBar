#!/usr/bin/env python

"""
Here are some general use utils that are used throughout the code.
"""

__all__ = ['unquote']

def unquote(string):
    """Removes double quotes from string

    >>> unquote('"hello"')
    'hello'

    If there is only one double quote let's not remove it.

    >>> unquote('"hel')
    '"hel'
    """

    if string.startswith('"') and string.endswith('"'):
        return string[1:-1]
    return string


if __name__ == "__main__":
    import doctest
    doctest.testmod()
