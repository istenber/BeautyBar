#!/usr/bin/env python
"""
Here are Data and Item classes that handle all data use, store,
validation and modifications.
"""

import logging

from model.utils import unquote


max_items=6


def to_float(value):
    """ Convert value to float

      >>> type(to_float('1234'))
      <type 'float'>

      >>> type(to_float('not a value'))
      <type 'float'>

    """
    try:
        return float(value)
    except ValueError, er:
        return 0.0


class Item(object):
    """
    Simple use of item...

      >>> unicode(Item(name='ilpo', value='20', row=3))
      u'name: ilpo, value: 20.0, row 3'

    It defaults to some values...

      >>> unicode(Item(value='incorrect'))
      u'name: no name, value: 0.0, row 1'

    And does not allow too big row numbers...

      >>> unicode(Item(row=20))
      ...
      Traceback (most recent call last):
      ...
      ValueError: Incorrect row: 20

    """

    def __init__(self, name = 'no name', value = 0.0, row = 1):
        self.set_name(name)
        self.set_value(value)
        self.set_row(row)

    def set_name(self, name):
        self.name = name

    def set_value(self, value):
        self.value = to_float(value)

    def set_row(self, row):
        if row <= 0 or row > max_items:
            raise ValueError('Incorrect row: ' + str(row))
        self.row = row

    def __cmp__(self, other):
        return cmp(self.row, other.row)

    def __unicode__(self):
        return 'name: %s, value: %s, row %s' % (self.name, self.value, self.row)


class Data(object):
    """ Data is kind of array containing list of items, some range values
    and checks to verify them.

      >>> unicode(Data())
      u'name: no name (0.0, 50.0)'

    There is class method to get default datas...

      >>> unicode(Data.default())
      u'name:  (0.0, 50.0)'

    """

    def __init__(self, name = 'no name', min = 0.0, max = 50.0, locked = False):
        self.name = name
        self.locked = locked
        self.min = min
        self.max = max
        self.items = []

    # boilerplate ---------------------------
    def _add_item(self, item):
        return self.items.append(item)

    def get_items(self):
        return self.items

    # TODO: make general super class with this method
    # TODO: this needs be made nicer, and better
    #       now it only works for classes in same file
    @classmethod
    def objfac(cls, new_cls, **kwds):
        return eval(new_cls)(**kwds)
    # ---------------------------------------

    def is_valid(self):
        item_count = len(self.get_items())
        if item_count != self.max_len():
            logging.info('Wrong number of items: ' + str(item_count))
            return False
        if not self._all_in_range(self.min, self.max):
            logging.info('Some items out of range')
            return False
        return True

    def value_ok(self, value, min = None, max = None):
        try:
            value = float(value)
        except ValueError:
            return False
        if min is None: min = self.min
        if max is None: max = self.max
        # logging.debug('Range: ' + str(min) + ' < ' + str(value) + ' < ' +
        #               str(max) + ' is ' + str(value <= max and value >= min))
        return (value <= max and value >= min)

    # TODO: fix item additions to use this
    def add_item(self, item):
        if len(self.get_items()) < self.max_len():
            if self.value_ok(item.value):
                self._add_item(item)
                return True
            else:
                logging.debug('Object (' + item.name + ':' +
                             str(item.value) + ') not in range')
                return False
        else:
            logging.debug('Too many objects')
            return False

    def _all_in_range(self, min, max):
        for item in self.get_items():
            if not self.value_ok(item.value, min, max):
                return False
        return True

    def _set_limit(self, limit, val):
        try:
            val = float(val)
        except ValueError, er:
            logging.info(str(limit) + ': \"' + str(max) + '\" is not float')
            return getattr(self, limit)
        if limit == 'min':
            is_valid = self._all_in_range(val, self.max)
        elif limit == 'max':
            is_valid = self._all_in_range(self.min, val)
        else:
            raise Exception('Unknown limit: ' + str(limit))
        if is_valid:
            setattr(self, limit, val)
        else:
            logging.info('Try to set ' + str(limit) +
                         ' while some items leave out')
        return getattr(self, limit)

    def set_max(self, max):
        return self._set_limit('max', max)

    def set_min(self, min):
        return self._set_limit('min', min)

    def as_list(self):
        # TODO: is this needed as we have __cmp__ in items
        return sorted(self.get_items(), lambda a, b: int(a.row - b.row))

    def to_generator(self, generator):
        if not self.is_valid():
            logging.info('Invalid')
        for item in self.as_list():
            # TODO: use row index
            generator.add_row(item.name, item.value)
        generator.set_range(self.min, self.max)

    @classmethod
    def max_len(cls):
        return max_items

    @classmethod
    def default(cls):
        d = cls.objfac('Data', name = '', min = 0.0, max = 50.0, locked = False)
        d.add_item(cls.objfac('Item', name='a', value=10.0, row=1))
        d.add_item(cls.objfac('Item', name='b', value=15.0, row=2))
        d.add_item(cls.objfac('Item', name='c', value=20.0, row=3))
        d.add_item(cls.objfac('Item', name='d', value=30.0, row=4))
        d.add_item(cls.objfac('Item', name='e', value=40.0, row=5))
        d.add_item(cls.objfac('Item', name='f', value=50.0, row=6))
        return d

    # Not fully compliant with csv, as ...
    # 1. 'e accept following separators ,.:\t
    # 2. Don't allow multiline messages
    # 3. Allow only lines with two values, all others are ignored
    @classmethod
    def parse_csv(cls, csv):
        lines = []
        for line in csv.splitlines():
            if line.strip() == '': continue
            lines.append(line)
        if len(lines) < cls.max_len():
            logging.debug('Too few lines (' + str(len(lines)) + ') in CSV')
            return None
        for delim in [',', '.', ':', '\t']:
            d = cls.objfac('Data', name='', min=0.0, max=50.0, locked=False)
            line_nro = 1
            for line in lines:
                try:
                    vals = line.split(delim)
                except ValueError, e:
                    logging.debug('Error in CSV line: \"' + line + '\"')
                    return None
                if len(vals) == 2:
                    name = unquote(vals[0])
                    item = cls.objfac('Item', name=name, row=line_nro)
                    if not d.value_ok(unquote(vals[1])):
                        logging.debug('Value not acceptable')
                        return None
                    item.set_value(vals[1])
                    if not d.add_item(item):
                        logging.debug('Incorrect item')
                        return None
                    else:
                        line_nro += 1
            if d.is_valid(): return d
        logging.debug('Cannot parse CSV')
        return None

    @classmethod
    def from_arrays(cls, min, max, names, values):
        d = cls.objfac('Data', name='', min=0.0, max=50.0, locked=False)
        d.set_min(min)
        d.set_max(max)
        for row in range(0, cls.max_len()):
            item = cls.objfac('Item', name=names[row], row=row)
            if not d.value_ok(unquote(values[row])):
                logging.debug('Value not accetable')
                return None
            item.set_value(values[row])
            if not d.add_item(item):
                logging.debug('Incorrect item')
                return None
        if not d.is_valid():
            return None
        return d

    def __unicode__(self):
        return 'name: %s (%s, %s)' % (self.name, self.min, self.max)


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.DEBUG)
    import doctest
    doctest.testmod()

