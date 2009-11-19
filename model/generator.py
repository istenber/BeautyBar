#!/usr/bin/env python

import logging

class Generator(object):
    def __init__(self, name=""):
        self.name = name
        self.active = "false" # TODO: fix to boolean
        self.attributes = []

class Attribute(object):
    def __init__(self, name="", value=""):
        self.name = name
        self.value = value


def main():
    logging.getLogger().setLevel(logging.DEBUG)
    g = Generator(name="gene")
    a = Attribute(name="color", value="red")
    g.attributes.append(a)
    print "g: " + str(g)    
    print "a: " + str(a)

if __name__ == "__main__":
    main()
