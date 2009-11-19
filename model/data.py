#!/usr/bin/env python

import logging

class Item(object):

    def __init__(self, name="", value="", row=""):
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

    def is_in_range(self, min, max):
        return (self.value <= max and self.value >= min)


class Data(object):

    def __init__(self, name="", min=0, max=50):
        self.name = name
        self.locked = "false" # TODO: fix to boolean
        self.min = min
        self.max = max
        self.items = []

    def add_item(self, item):
        if len(self.items) < 6:
            if item.is_in_range(self.min, self.max):
                self.items.append(item)
            else:
                logging.info("# Object not in range")
        else:
            logging.info("# Too many objects")

    def set_item(self, index, item):
        if index < 0 or index > 5: return False
        if item.is_in_range(self.min, self.max):
            self.items[index] = item

    def _all_in_range(self, min, max):
        for item in self.items:
            if not item.is_in_range(min, max):
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

    @staticmethod
    def default():
        d = Data()
        d.add_item(Item("a", "10"))
        d.add_item(Item("b", "15"))
        d.add_item(Item("c", "20"))
        d.add_item(Item("d", "30"))
        d.add_item(Item("e", "40"))
        d.add_item(Item("f", "50"))
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
