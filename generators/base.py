#!/usr/bin/env python2.5

if __name__ == '__main__':
    import sys
    sys.path.append('/home/sankari/dev/beautybar')


from gui_interface import GuiInterface
from process_interface import ProcessInterface
from model.number_scaler import NumberScaler


class BaseGenerator(GuiInterface, ProcessInterface):

    def __init__(self):
        self.rows = []

    def set_range(self, min, max):
        self.min = float(min)
        self.max = float(max)

    def add_row(self, name, value):
        self.rows.append([name, value])

    def get_row_count(self):
        return len(self.rows)

    def get_row_name(self, row, max_len=6):
        """ Return name with max 10 chars

          >>> b = BaseGenerator()
          >>> b.add_row('what a nice day today', 123456)
          >>> b.get_row_name(0)
          'what..'
          >>> b.add_row('title', 111)
          >>> b.get_row_name(1)
          'title'

        """
        name = self.rows[row][0]
        if len(name) > max_len:
            name = name[:(max_len - 2)] + '..'
        return name

    def get_row_value(self, row):
        """ Return value in range 0.0..1.0

          >>> b = BaseGenerator()
          >>> b.set_range(0, 1000)
          >>> b.add_row('what a nice day today', 1000)
          >>> b.get_row_value(0)
          1.0
          >>> b.set_range(500, 1000)
          >>> b.add_row('another', 750)
          >>> b.get_row_value(1)
          0.5

        """
        return (self.rows[row][1] - self.min) / (self.max - self.min)


    def get_row_value_str(self, row, max_len=10):
        """ Return value name with max 10 chars

          >>> b = BaseGenerator()
          >>> b.set_range(0, 1000)
          >>> b.add_row('what a nice day today', 1000)
          >>> b.get_row_value_str(0)
          '1k'

        """
        return NumberScaler().scale(self.rows[row][1],
                                    round=False)

    def get_scale_str(self, pos, max_len=10):
        """ Return scale string for position,
        position should be in range 0.0 ... 1.0

          >>> b = BaseGenerator()
          >>> b.set_range(0, 10000)
          >>> b.get_scale_str(0.5)
          '5k'
          >>> b.get_scale_str(0.22)
          '2k'

        """
        return NumberScaler().scale(pos * (self.max - self.min) + self.min,
                                    round=False)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
