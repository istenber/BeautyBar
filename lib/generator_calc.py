#!/usr/bin/env python2.5

"""
Calculate various widths and bar sizes for generators, for example...

If we have default size image (300x200) with default bar count (6), and
we want to have edges size 10px. Note: actual edge is equal or greater
then succested edge. Chart should look like: 12 - 23/35 - 69/81 - ... - 12

  >>> g = GeneratorCalc()
  >>> g.calc(edge_width=11)
  >>> g.edge_width
  12
  >>> g.left(0)
  23
  >>> g.left(3)
  161
  >>> g.middle(1)
  81

Another example with more bars and values set in constructor

  >>> g = GeneratorCalc(edge_width=20)
  >>> g(bar_count=10)
  >>> g.left(3)
  104
  >>> g.left(2)
  78
  >>> g.middle(4)
  137

Sometimes we need also width of chart area, for example to draw background

  >>> g = GeneratorCalc()
  >>> g.calc()
  >>> g.edge_width
  12
  >>> g.area
  276

Fontsize
  
  >>> g = GeneratorCalc()
  >>> g.calc(font_size = 12, bar_count = 10)
  >>> g.font_size
  10

"""

import logging


class GeneratorCalc(object):

    def __init__(self, **kwds):
        self._defaults()
        self._handle_kwds(kwds)

    def calc(self, **kwds):
        self._handle_kwds(kwds)
        self.area = self.chart_width - self.edge_width * 2
        self.bar_area = self.area / self.bar_count
        self.edge_width += self.area % self.bar_count / 2
        self.area = self.chart_width - self.edge_width * 2
        self.bar_width = int(self.bar_area * self.bar_size / 100.0)
        self.font_size = min(int((5 + 30.0 / self.bar_count) *
                                 self.font_size / 12.0), self.font_size)
        s0 = int(self.edge_width + self.bar_area *
                 (1 - self.bar_size / 100.0) / 2)
        self.l = map(lambda i: int(i * self.bar_area + s0),
                     range(0, self.bar_count))
        sm = int(self.edge_width + self.bar_area * 0.5)
        self.m = map(lambda i: int(i * self.bar_area + sm),
                     range(0, self.bar_count))

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
        self.chart_width = 300    # (px) chart width
        self.edge_width = 10      # (px) space in edge
        self.font_size = 12

    def _check_bounds(self, index):
        if index < 0 or index >= self.bar_count:
            logging.error("Index out of bounds: %d" % index)
            return False
        return True

    def _handle_kwds(self, kwds):
        for key in kwds.iterkeys():
            if hasattr(self, key):
                self.__dict__[key] = kwds[key]
            else:
                logging.info("Unknow key: %s" % key)

    __call__ = calc


def main():
    logging.getLogger().setLevel(logging.DEBUG)
    import doctest
    doctest.testmod()

if __name__ == '__main__':
    main()
