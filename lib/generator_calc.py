#!/usr/bin/env python2.5

"""
Calculate various widths and bar sizes for generators, for example...

If we have default size image (300x200) with default bar count (6), and
we want to have edges size 10px. Note: actual edge is equal or greater
then succested edge. Chart should look like: 12 - 23/35 - 69/81 - ... - 12

  >>> g = GeneratorCalc(edge=10)
  >>> g.get('edge')
  12
  >>> g.left(0)
  23
  >>> g.left(3)
  161
  >>> g.middle(1)
  81

Another example with more bars:

  >>> g = GeneratorCalc(bar_count=10)
  >>> g.left(3)
  101
  >>> g.left(2)
  73
  >>> g.middle(4)
  136

Sometimes we need also width of chart area, for example to draw background

  >>> g = GeneratorCalc()
  >>> g.get('edge')
  12
  >>> g.get('area')
  276
  
"""

import logging


class GeneratorCalc(object):

    def __init__(self, **kw):
        self._defaults()        
        w = self.w
        keys = w.keys()
        for key in kw.iterkeys():
            if key in keys:
                w[key] = int(kw[key])
            elif hasattr(self, key):
                self.__dict__[key] = kw[key]
            else:
                logging.info("Unknow key: %s" % key)
        w['area'] = w['chart'] - w['edge'] * 2
        w['bar_area'] = w['area'] / self.bar_count
        w['edge'] += w['area'] % self.bar_count / 2
        w['area'] = w['chart'] - w['edge'] * 2 # recalc with new edge value
        s0 = int(w['edge'] + w['bar_area'] * (1 - self.bar_size / 100.0) / 2)
        self.l = map(lambda i: int(i * w['bar_area'] + s0),
                     range(0, self.bar_count))
        sm = int(w['edge'] + w['bar_area'] * 0.5)
        self.m = map(lambda i: int(i * w['bar_area'] + sm),
                     range(0, self.bar_count))


    def get(self, attr):
        if attr in self.w.keys():
            return self.w[attr]
        logging.error("Try to get missing key: %s" % key)
        return 0

    def middle(self, index):
        if self._check_bounds(index):
            return self.m[index]
        return 0

    def left(self, index):
        if self._check_bounds(index):
            return self.l[index]
        return 0

    def _defaults(self):
        self.bar_count = 6
        self.bar_size = 50        # (%)  bar size of bar space
        self.w = {'chart' : 300,  # (px) chart width
                  'edge'  : 10,   # (px) space in edge
                  }

    def _check_bounds(self, index):
        if index < 0 or index >= self.bar_count:
            logging.error("Index out of bounds: %d" % index)
            return False
        return True


def main():
    logging.getLogger().setLevel(logging.DEBUG)
    import doctest
    doctest.testmod()

if __name__ == '__main__':
    main()
