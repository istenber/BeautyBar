#!/usr/bin/env python

import logging

class Generator(object):

    def __init__(self, name=""):
        self.name = name
        self.active = False
        self.attributes = []

    def copy(self):
        g = Generator()
        g.name = self.name
        g.active = self.active
        g.attributes = []
        for attr in self.attributes:
            g.attributes.append(attr.copy())
        return g

    def get_attribute(self, name):
        for attr in self.attributes:
            if attr.name == name: return attr
        a = Attribute(name=name)
        self.attributes.append(a)
        return a


class Attribute(object):

    def __init__(self, name="", value=""):
        self.name = name
        self.value = value

    def copy(self):
        a = Attribute()
        a.name = self.name
        a.value = self.value
        return a


def main():
    logging.getLogger().setLevel(logging.DEBUG)
    g = Generator(name="gene")
    a = Attribute(name="color", value="red")
    g.attributes.append(a)
    print "g: " + str(g)    
    print "a: " + str(a)

if __name__ == "__main__":
    main()
