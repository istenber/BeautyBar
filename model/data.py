#!/usr/bin/env python

import logging

from model.utils import unquote


def to_float(value):
    try:
        out = float(value)
    except ValueError, er:
        out = 0
    return out


class Item(object):

    def __init__(self, name="", value=0, row=0):
        self.name = name
        self.value = to_float(value)
        # TODO: row range?!
        self.row = row

    def set_name(self, name):
        self.name = name

    def set_value(self, value):
        self.value = to_float(value)

    def set_row(self, name):
        self.row = int(row)

    def __cmp__(self, other):
        return cmp(self.row, other.row)


class Data(object):

    def __init__(self, name="", min=0.0, max=50.0):
        self.name = name
        self.locked = False
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
            logging.info("# Wrong number of items: " + str(item_count))
            return False
        if not self._all_in_range(self.min, self.max):
            logging.info("# Some items out of range")
            return False
        return True

    def value_ok(self, value, min=None, max=None):
        try:
            value = float(value)
        except ValueError, er:
            # logging.info("# value is not float: " + str(value))
            return False
        if min is None: min = self.min
        if max is None: max = self.max
        # logging.info("# range: " + str(min) + " < " + str(value) + " < " +
        #              str(max) + " is " + str(value <= max and value >= min))
        return (value <= max and value >= min)

    # TODO: fix item additions to use this
    def add_item(self, item):
        if len(self.get_items()) < self.max_len():
            if self.value_ok(item.value):
                self._add_item(item)
                return True
            else:
                logging.info("# Object (" + item.name + ":" +
                             str(item.value) + ") not in range")
                return False
        else:
            logging.info("# Too many objects")
            return False

    def _all_in_range(self, min, max):
        for item in self.get_items():
            if not self.value_ok(item.value, min, max):
                return False
        return True

    def set_max(self, max):
        try:
            max = float(max)
        except ValueError, er:
            logging.info("# max: \"" + str(max) + "\" is not float")
            return self.max
        if self._all_in_range(self.min, max):
            self.max = max
        else:
            logging.info("# Try to set max too low?")
        return self.max

    def set_min(self, min):
        try:
            min = float(min)
        except ValueError, er:
            logging.info("# min: \"" + str(min) + "\" is not float")
            return self.max
        if self._all_in_range(min, self.max):
            self.min = min
        else:
            logging.info("# Try to set min too high?")
        return self.min

    def as_list(self):
        return sorted(self.get_items(), lambda a, b: int(a.row - b.row))

    def to_generator(self, generator):
        if not self.is_valid():
            logging.info("# Invalid")
        for item in self.as_list():
            # TODO: use row index
            generator.add_row(item.name, item.value)
        generator.set_range(self.min, self.max)

    @classmethod
    def max_len(cls):
        return 6

    @classmethod
    def default(cls):
        d = cls.objfac('Data', name="", min=0.0, max=50.0, locked=False)
        d.add_item(cls.objfac('Item', name="a", value=10.0, row=1))
        d.add_item(cls.objfac('Item', name="b", value=15.0, row=2))
        d.add_item(cls.objfac('Item', name="c", value=20.0, row=3))
        d.add_item(cls.objfac('Item', name="d", value=30.0, row=4))
        d.add_item(cls.objfac('Item', name="e", value=40.0, row=5))
        d.add_item(cls.objfac('Item', name="f", value=50.0, row=6))
        return d

    # Not fully compliant with csv, as ...
    # 1. "e accept following separators ,.:\t
    # 2. Don't allow multiline messages
    # 3. Allow only lines with two values, all others are ignored
    @classmethod
    def parse_csv(cls, csv):
        lines = []
        for line in csv.splitlines():
            if line.strip() == "": continue
            lines.append(line)
        if len(lines) < cls.max_len():
            logging.info("# Too few lines (" + str(len(lines)) + ") in CSV")
            return None
        for delim in [",", ".", ":", "\t"]:
            d = cls.objfac('Data', name="", min=0.0, max=50.0, locked=False)
            line_nro = 1
            for line in lines:
                try:
                    vals = line.split(delim)
                except ValueError, e:
                    logging.info("# Error in CSV line: \"" + line + "\"")
                    return None
                if len(vals) == 2:
                    name = unquote(vals[0])
                    item = cls.objfac('Item', name=name, row=line_nro)
                    d.value_ok(unquote(vals[1]))
                    item.set_value(vals[1])
                    if not d.add_item(item):
                        logging.info("# Incorrect item")
                        return None
                    else:
                        line_nro += 1
            if d.is_valid(): return d
        logging.info("# Cannot parse CSV")
        return None


class TestGenerator(object):
    def add(self, name, value):
        print "name: " + str(name) + "\tvalue: " + str(value)


def main():
    logging.getLogger().setLevel(logging.DEBUG)
    d = Data.default()
    print "\n  # data:      \n" + str(d)
    print "\n  # as_list:   \n" + str(d.as_list())
    print "\n  # generator: \n"
    d.to_generator(TestGenerator())
    d.add_item(Item("one", "60"))
    i = Item("ilpo", "xx")
    print "\n  # item(xx) \nn:" + str(i.name) + "\tv:" + str(i.value)
    i = Item("ilpo", "-2")
    print "\n  # item(-2) \nn:" + str(i.name) + "\tv:" + str(i.value)
    i = Item("ilpo", "99")
    print "\n  # item(99) \nn:" + str(i.name) + "\tv:" + str(i.value)
    d.set_min(10)
    d.set_max(99)
    print "\n  # max: " + str(d.max)

if __name__ == "__main__":
    main()
