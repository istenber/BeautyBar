#!/usr/bin/env python

import logging


class Item(object):

    def __init__(self, name="", value=0, row=0):
        self.name = name
        self.value = self._to_int(value)
        # TODO: row range?!
        self.row = row
        
    def _to_int(self, value):
        try:
            out = int(value)
        except ValueError, er:
            out = 0
        return out

    def set_name(self, name):
        self.name = name

    def set_value(self, value):
        self.value = self._to_int(value)

    def set_row(self, name):
        self.row = self._to_int(row)

    def copy(self):
        i = Item()
        i.name = self.name
        i.value = self.value
        i.row = self.row
        return i


class Data(object):

    def __init__(self, name="", min=0, max=50):
        self.name = name
        self.locked = False
        self.min = min
        self.max = max
        self.items = []

    def value_ok(self, value, min=None, max=None):
        try:
            value = int(value)
        except ValueError, er:
            # logging.info("# value is not integer: " + str(value))
            return False
        if min is None: min = self.min
        if max is None: max = self.max
        # logging.info("# range: " + str(min) + " < " + str(value) + " < " +
        #              str(max) + " is " + str(value <= max and value >= min))
        return (value <= max and value >= min)

    def add_item(self, item):
        if len(self.items) < 6:
            if self.value_ok(item.value):
                self.items.append(item)
            else:
                logging.info("# Object not in range")
        else:
            logging.info("# Too many objects")

    def _all_in_range(self, min, max):
        for item in self.items:
            if not self.value_ok(item.value, min, max):
                return False
        return True

    def set_max(self, max):
        if self._all_in_range(self.min, max):
            self.max = max
        else:
            logging.info("# Try to set max too low?")

    def set_min(self, min):
        if self._all_in_range(min, self.max):
            self.min = min
        else:
            logging.info("# Try to set min too high?")

    def as_list(self):
        return self.items

    def to_generator(self, generator):
        # TODO: set scale/range!
        if len(self.items) != 6:
            logging.info("# Too few items: " + str(len(self.items)))
        for item in self.items:
            generator.add(item.name, item.value)

    def copy(self):
        d = Data()
        d.name = self.name
        d.locked = self.locked
        d.max = self.max
        d.min = self.min
        d.items = []
        for item in self.items:
            d.items.append(item.copy())
        return d

    @staticmethod
    def default():
        d = Data()
        d.items.append(Item("a", "10"))
        d.items.append(Item("b", "15"))
        d.items.append(Item("c", "20"))
        d.items.append(Item("d", "30"))
        d.items.append(Item("e", "40"))
        d.items.append(Item("f", "50"))
        return d
    
    def __str__(self):
        out = ""
        for item in self.items:
            out += str(item.name) + "\t" + str(item.value) + "\n"
        return out


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
