#!/usr/bin/env python

import logging

import generators
from model.utils import unquote
from model.decorator import Decorator
from model.data import Data


class Generator(object):

    def __init__(self, name=""):
        self.name = name
        self.attributes = []

    # boilerplate ---------------------------
    def add_attribute(self, attribute):
        return self.attributes.append(attribute)

    def get_attributes(self):
        return self.attributes

    @classmethod
    def objfac(cls, new_cls, **kwds):
        return eval(new_cls)(**kwds)
    # ---------------------------------------

    def _attribute_with_default_value(self, name):
        v = self.me().get_attribute(name).get_value()
        return self.objfac('Attribute', name=name, value=v)

    def get_attribute(self, name):
        """ Read only version of get_attribute """
        for attr in self.get_attributes():
            if attr.name == name:
                return attr
        return self._attribute_with_default_value(name)

    def get_rw_attribute(self, name):
        """ Read/write version of get_attribute """
        for attr in self.get_attributes():
            if attr.name == name:
                return attr
        attr = self._attribute_with_default_value(name)
        self.add_attribute(attr)
        return attr

    def build_chart(self, data):
        chart = self.me()
        for attr in chart.get_attributes():
            v = unquote(self.get_attribute(attr.get_name()).value)
            if v != "":
                attr.set_value(v)
        if not data.is_valid():
            logging.info('Invalid')
            data = Data.default()
        for item in data.as_list():
            chart.add_row(item.name, item.value)
        chart.set_range(data.min, data.max)
        return Decorator(chart)

    def me(self):
        return generators.get_instance(self.name)

    @classmethod
    def error(cls, msg):
        chart = generators.get_error_instance()
        chart.set_msg(msg)
        return Decorator(chart)


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
