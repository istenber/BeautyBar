#!/usr/bin/env python

class Item(object):

    def __init__(self, name, value):
        self.name  = self._validate_name(name)
        self.value = self._validate_value(value)

    def _validate_name(self, name):
        return name

    def _validate_value(self, value):
        try:
            v = int(value)
        except ValueError:
            v = 0
        if v < 0:
            return 0
        if v > 50:
            return 50
        return v

class Data(object):

    def __init__(self):
        self.items = []

    def add_item(self, item):
        if len(self.items) < 6:
            self.items.append(item)
        else:
            pass

    def as_list(self):
        return self.items

    def to_generator(self, generator):
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

if __name__ == "__main__":
    main()
