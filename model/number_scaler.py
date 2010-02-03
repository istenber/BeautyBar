#!/usr/bin/env python
"""
Number scaler is used to scale numbers to shorter ones...

  >>> n = NumberScaler()
  >>> n.scale(100000)
  '100k'

It accepts both strings, ints and floats as input

  >>> n = NumberScaler()
  >>> n.scale(float(10.20))
  '10'
  >>> n.scale('1000')
  '1k'

It scales so that only one number matters, but with roundings

  >>> n = NumberScaler()
  >>> n.scale(24345)
  '20k'
  >>> n.scale(2655)
  '3k'
  >>> n.scale(29055)
  '30k'

It support thousands, millions, billions

  >>> n = NumberScaler()
  >>> n.scale(4000)
  '4k'
  >>> n.scale(40000000)
  '40m'
  >>> n.scale(400000000000)
  '400b'

Returns empty string with error values

  >>> n = NumberScaler()
  >>> n.scale('hello world')
  ''

If you do not want to round last number use option round = False

  >>> n = NumberScaler()
  >>> n.scale(123456, round=False)
  '123k'
  >>> n.scale(123999, round=False)
  '124k'

Some more tests...

  >>> n = NumberScaler()
  >>> n.scale(309999, round=False)
  '310k'

"""

import logging


class NumberScaler(object):
    """ NumberScaler class
    """

    def scale(self, number, round=True):
        try:
            n = int(number)
        except ValueError:
            # TODO: should we throw exception instead
            return ''
        for (scale, s) in [(1000000000, 'b'), (1000000, 'm'), (1000, 'k')]:
            if n >= scale:
                n = n / ( scale / 10 )
                n = self.nround(n)
                if round:
                    out = s
                    p = 0
                    while n / 10 > 0:
                        out = '0' + out
                        n = self.nround(n)
                    return str(n) + out
                else:
                    return str(n) + s
        return str(n)
    
    def nround(self, val):
        """ Rounding function """
        if val % 10 >= 5: return val / 10 + 1
        return val / 10
               

if __name__ == "__main__":
    # logging.getLogger().setLevel(logging.DEBUG)
    import doctest
    doctest.testmod()

