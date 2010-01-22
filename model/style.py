#!/usr/bin/env python

import logging

from model.generator import Generator
from model.generator_factory import GeneratorFactory


class Style(object):

    def __init__(self, name=""):
        self.name = name
        self.locked = False
        self.generators = []
        self.active_generator = None

    @classmethod
    def default(self):
        # TODO: add all default parameters
        s = self.objfac('Style', name= "default style")
        g = self.objfac('Generator', name="standard")
        s.add_generator(g)
        s.active_generator = g
        return s

    # boilerplate ---------------------------
    def add_generator(self, generator):
        return self.generators.append(generator)

    def get_generators(self):
        return self.generators

    @classmethod
    def objfac(self, cls, **kwds):
        # TODO: do we need more here?
        # if cls.__name__ == "Generator": return
        return eval(cls)(**kwds)
    # ---------------------------------------

    def get_active_generator(self):
        return self.active_generator

    def _find_generator(self, name):
        for g in self.get_generators():
            if g.name == name: return g
        return None

    def set_active_generator(self, name):
        g = self._find_generator(name)
        if not g:
            g = g = self.objfac('Generator', name=name)
            self.add_generator(g)
        self.active_generator = g

def main():
    pass

if __name__ == "__main__":
    main()
