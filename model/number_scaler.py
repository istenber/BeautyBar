#!/usr/bin/env python
"""
Number scaler is used to scale numbers to shorter ones...

  >>> NumberScaler().scale(100000)
  '100k'

It accepts both strings, ints and floats as input

  >>> NumberScaler().scale(float(10.20))
  '10'
  >>> NumberScaler().scale('1000')
  '1k'

It scales so that only one number matters, but with roundings

  >>> NumberScaler().scale(24345)
  '20k'
  >>> NumberScaler().scale(2655)
  '3k'
  >>> NumberScaler().scale(29055)
  '30k'

It support thousands, millions, billions

  >>> NumberScaler().scale(4000)
  '4k'
  >>> NumberScaler().scale(40000000)
  '40m'
  >>> NumberScaler().scale(400000000000)
  '400b'

Returns empty string with error values

  >>> NumberScaler().scale('hello world')
  ''

If you do not want to round last number use option round = False

  >>> NumberScaler().scale(123456, round=False)
  '123k'
  >>> NumberScaler().scale(123999, round=False)
  '124k'

Some more tests...

  >>> NumberScaler().scale(309999, round=False)
  '310k'

"""

import logging


from singleton import Singleton


class NumberScaler(Singleton):
    """ NumberScaler class
    """

    @classmethod
    def scale(cls, number, round=True):
        return cls.instance()._scale(number, round)

    def _scale(self, number, round=True):
        try:
            n = int(number)
        except ValueError:
            # TODO: should we throw exception instead
            return ''
        for (scale, s) in [(1000000000, 'b'), (1000000, 'm'), (1000, 'k')]:
            if n >= scale:
                n = n / ( scale / 10 )
                n = self._nround(n)
                if round:
                    out = s
                    p = 0
                    while n / 10 > 0:
                        out = '0' + out
                        n = self._nround(n)
                    return str(n) + out
                else:
                    return str(n) + s
        return str(n)
    
    def _nround(self, val):
        """ Rounding function """
        if val % 10 >= 5: return val / 10 + 1
        return val / 10
               

if __name__ == "__main__":
    # logging.getLogger().setLevel(logging.DEBUG)
    import doctest
    doctest.testmod()

