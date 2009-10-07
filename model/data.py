#!/usr/bin/env python

class Item(object):

    def __init__(self, name, value):
        self.name  = name
        self.value = value

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
        return Data([Item("a", "10"),
                     Item("b", "15"),
                     Item("c", "20"),
                     Item("d", "30"),
                     Item("e", "40"),
                     Item("f", "50"),
                     ])
    
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

if __name__ == "__main__":
    main()
