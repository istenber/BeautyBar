#!/usr/bin/env python

import logging

from model.generator_factory import GeneratorFactory
from model.utils import unquote
from model.decorator import Decorator


class Generator(object):

    def __init__(self, name=""):
        self.name = name
        self.active = False
        self.attributes = []
        self.factory = GeneratorFactory().instance()

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
        chart = self.factory.get_generator(self.name + ".py")
        v = chart.get_attribute(name).get_value()
        a = Attribute(name=name, value=v)
        self.attributes.append(a)
        return a

    def build_chart(self, data):
        chart = self.factory.get_generator(self.name + ".py")
        for attr in chart.get_attributes():
            v = unquote(self.get_attribute(attr.get_name()).value)
            if v != "":
                attr.set_value(v)
        data.to_generator(chart)
        return Decorator(chart)


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
