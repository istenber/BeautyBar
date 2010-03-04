#!/usr/bin/env python
"""
Here are Data and Item classes that handle all data use, store,
validation and modifications.
"""

import logging
import math

from model.utils import unquote


max_items=10
min_items=3


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

      >>> unicode(Data.default_simple())
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
        """ Is data set is full and valid to further processing.

          >>> d = Data()
          >>> d.is_valid()
          False
          >>> for i in range(1, 7):
          ...   d.add_item(Item())
          ...
          True
          True
          True
          True
          True
          True
          >>> d.is_valid()
          True

        """
        if not self.is_valid_len(len(self.get_items())):
            logging.info('Wrong number of items')
            return False
        if not self._all_in_range(self.min, self.max):
            logging.info('Some items out of range')
            return False
        return True

    def value_ok(self, value, min = None, max = None):
        """ Check that individual value is in range, autorange disables check

          >>> d = Data.default_simple()
          >>> d.value_ok(60)
          False
          >>> d.value_ok(20)
          True
          >>> d.value_ok(-10)
          False
          >>> d.autorange()
          >>> d.value_ok(-30)
          True

        """
        try:
            value = float(value)
        except ValueError:
            return False
        if min is None: min = self.min
        if max is None: max = self.max
        if hasattr(self, "autorange_on"): return True
        # logging.debug('Range: ' + str(min) + ' < ' + str(value) + ' < ' +
        #               str(max) + ' is ' + str(value <= max and value >= min))
        return (value <= max and value >= min)

    # TODO: fix item additions to use this
    def add_item(self, item):
        """ Add item to data set.

          >>> d = Data()
          >>> d.add_item(Item(value=10))
          True
          >>> d.add_item(Item(value=60)) # out of range
          False

        """
        if self.value_ok(item.value):
            self._add_item(item)
            return True
        else:
            logging.debug('Object (' + item.name + ':' +
                          str(item.value) + ') not in range')
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
        """ Set maximum limit range for data set, requires that current items
        are in range. Returns limit after change.

          >>> d = Data()
          >>> d.max
          50.0
          >>> d.set_max(30)
          30.0
          >>> d.max
          30.0
          >>> d = Data.default_simple()
          >>> d.set_max(30) # there are items with higher values
          50.0

        """
        return self._set_limit('max', max)

    def set_min(self, min):
        """ Set minimum limit range. Same as set_max() but with minimum,
        no negative values accepted.

          >>> d = Data()
          >>> d.set_min(-10)
          0.0

        """
        if min < 0: return self.min
        return self._set_limit('min', min)

    def as_list(self):
        """ Returns items as sorted list. Uses Item.__cmp__() to sort.

          >>> d = Data.default_simple()
          >>> for i in d.as_list():
          ...   unicode(i)
          u'name: a, value: 10.0, row 1'
          u'name: b, value: 15.0, row 2'
          u'name: c, value: 20.0, row 3'
          u'name: d, value: 30.0, row 4'
          u'name: e, value: 40.0, row 5'
          u'name: f, value: 50.0, row 6'
          u'name: g, value: 40.0, row 7'
          u'name: h, value: 30.0, row 8'
          u'name: i, value: 20.0, row 9'
          u'name: j, value: 10.0, row 10'

        """
        return sorted(self.get_items())

    def autorange(self):
        """Autorange set range automatically to correct values

          >>> d = Data()
          >>> d.is_valid()
          False
          >>> d.autorange()
          >>> d.add_item(Item(value=70))
          True
          >>> d.autorange()
          >>> d.min
          0.0
          >>> d.max
          100.0
          >>> d.autorange()
          >>> d.add_item(Item(value=350))
          True
          >>> d.autorange()
          >>> d.max
          1000.0
          >>> d.autorange()
          >>> d.add_item(Item(value=4891))
          True
          >>> unicode(d)
          u'name: no name (autorange)'
          >>> d.autorange()
          >>> d.max
          10000.0
          >>> unicode(d)
          u'name: no name (0.0, 10000.0)'

        """
        if not hasattr(self, "autorange_on"):
            self.autorange_on = True
            return
        self.min = 0.0
        m = max(self.get_items(), key=lambda x: x.value)
        n = math.pow(10, math.floor(math.log(m.value, 10)) + 1)
        self.max = math.ceil(m.value / n) * n
        del self.autorange_on
        return

    @classmethod
    def max_len(cls):
        """ Max lenght of items """
        return max_items

    @classmethod
    def min_len(cls):
        """ Min lenght of items """
        return min_items

    @classmethod
    def is_valid_len(cls, amount):
        """ Valid amount of items """
        return amount >= min_items and amount <= max_items

    @classmethod
    def default_simple(cls):
        """ Return default data

          >>> d = Data.default_simple()
          >>> d.get_items()[1].value
          15.0

        """
        return cls.default_data_set([['a', 10.0], ['b', 15.0], ['c', 20.0],
                                     ['d', 30.0], ['e', 40.0], ['f', 50.0],
                                     ['g', 40.0], ['h', 30.0], ['i', 20.0],
                                     ['j', 10.0]],
                                    min = 0.0, max = 50.0)

    @classmethod
    def default_google(cls):
        """ Return default data

          >>> d = Data.default_google()
          >>> d.get_items()[3].value
          657.0

        """
        return cls.default_data_set([['2005', 193.0], ['2006', 465.0],
                                     ['2007', 505.0], ['2008', 657.0],
                                     ['2009', 315.0], ['2010', 602.0]],
                                    min = 0.0, max = 1000.0)

    @classmethod
    def default_clean(cls):
        """ Return default data

          >>> d = Data.default_clean()
          >>> d.get_items()[4].value
          0.0

        """
        return cls.default_data_set([['', 0.0], ['', 0.0], ['', 0.0],
                                     ['', 0.0], ['', 0.0], ['', 0.0]],
                                    min = 0.0, max = 100.0)

    default=default_google

    @classmethod
    def default_data_set(cls, items, min = min, max = max):
        """ Takes data in raw format and returns Data """
        s = cls.objfac('Data', name = '', min = min, max = max, locked = False)
        if not cls.is_valid_len(len(items)):
            logging.info("Wrong amount of default data")
            return None
        for i in range(0, len(items)):
            s.add_item(cls.objfac('Item', row = i + 1,
                                  name = items[i][0], value = items[i][1]))
        return s

    @classmethod
    def read_datasource(cls, datasource):
        """ Read data from datasource and create Data object based on it.

          >>> class TestDataSource(object):
          ...  def is_ok(self): return True
          ...  def get_rows(self):
          ...    return [['a', '1'], ['b', '2'], ['c', '3'],
          ...            ['d', '4'], ['e', '5'], ['f', '6']]
          ...
          >>> d = Data.read_datasource(TestDataSource())
          >>> d.get_items()[3].value
          4.0
          >>> d.get_items()[2].name
          'c'

        """
        d = cls.objfac('Data', name='', min=0.0, max=50.0, locked=False)
        d.autorange()
        line_nro = 1
        if not datasource.is_ok():
            logging.info("Datasource valid")
            return None
        rows = datasource.get_rows()
        if not cls.is_valid_len(len(rows)):
            logging.info("Wrong number of rows")
            return None
        if len(rows[0]) != 2:
            logging.info("Wrong number of columns")
            return None
        for row in rows:
            item = cls.objfac('Item', name=row[0], row=line_nro)
            if not d.value_ok(row[1]):
                return None
            item.set_value(row[1])
            if not d.add_item(item):
                return None
            else:
                line_nro += 1
        if not d.is_valid():
            return None
        d.autorange()
        return d

    # Not fully compliant with csv, as ...
    # 1. 'e accept following separators ,.:\t
    # 2. Don't allow multiline messages
    # 3. Allow only lines with two values, all others are ignored
    @classmethod
    def parse_csv(cls, csv):
        """ Parse comma separated values (csv) to data object.

          >>> csv = 'a,10\\nb,20\\nc,30\\nd,40\\ne,50\\nf,15\\n'
          >>> d = Data.parse_csv(csv)
          >>> for i in d.as_list():
          ...   print unicode(i)
          ...
          name: a, value: 10.0, row 1
          name: b, value: 20.0, row 2
          name: c, value: 30.0, row 3
          name: d, value: 40.0, row 4
          name: e, value: 50.0, row 5
          name: f, value: 15.0, row 6

        Incorrect csvs returns None value

          >>> empty_csv = 'nothing here'
          >>> print Data.parse_csv(empty_csv) # print or None is not shown
          None

        """
        lines = []
        for line in csv.splitlines():
            if line.strip() == '': continue
            lines.append(line)
        for delim in [',', '.', ':', '\t']:
            d = cls.objfac('Data', name='', min=0.0, max=50.0, locked=False)
            d.autorange()
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
            if d.is_valid():
                d.autorange()
                return d
        logging.debug('Cannot parse CSV')
        return None

    @classmethod
    def from_arrays(cls, min, max, names, values):
        """ Build data set from name and value arrays.

          >>> n = ['a', 'b', 'd', 'e', 'f', 'h']
          >>> v = [1, 2, 3, 4, 5, 6]
          >>> d = Data.from_arrays(0, 10, n, v)
          >>> for i in d.as_list():
          ...   print unicode(i)
          ...
          name: a, value: 1.0, row 1
          name: b, value: 2.0, row 2
          name: d, value: 3.0, row 3
          name: e, value: 4.0, row 4
          name: f, value: 5.0, row 5
          name: h, value: 6.0, row 6

        Or with error case...

          >>> print Data.from_arrays(0, 10, [], [])
          None

        """
        # TODO: why not set min and max in constructor
        d = cls.objfac('Data', name='', min=0.0, max=50.0, locked=False)
        # these are needed as min and max might not be floats by default
        d.set_min(min)
        d.set_max(max)
        l = len(names)
        if not cls.is_valid_len(l):
            logging.debug('Wrong size array')
            return None
        if l != len(values):
            logging.debug('Different size arrays')
            return None
        for row in range(0, l):
            value = values[row]
            if not d.value_ok(value):
                value = unquote(value)
            if not d.value_ok(value):
                logging.debug('Value not accetable')
                return None
            item = cls.objfac('Item', name=names[row], value=0.0, row=row+1)
            # we have use set_value, as it converts values to float and
            # current databasemapper prevents constructor to do it
            item.set_value(value)
            if not d.add_item(item):
                logging.debug('Incorrect item')
                return None
        if not d.is_valid():
            return None
        return d

    def __unicode__(self):
        if hasattr(self, "autorange_on"):
            return 'name: %s (autorange)' % (self.name)
        return 'name: %s (%s, %s)' % (self.name, self.min, self.max)


if __name__ == "__main__":
    # logging.getLogger().setLevel(logging.DEBUG)
    import doctest
    doctest.testmod()

