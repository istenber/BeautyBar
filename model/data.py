#!/usr/bin/env python

class Item(object):

    def __init__(self, name, value):
        self.name  = name
        self.value = value

class Data(object):

    def __init__(self, items=[]):
        self.items = items

    def add_item(self, item):
        self.items.append(item)

    def as_list(self):
        return self.items

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

def main():
    d = Data.default()
    print "data: \n" + str(d)

if __name__ == "__main__":
    main()
