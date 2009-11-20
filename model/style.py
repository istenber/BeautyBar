#!/usr/bin/env python

import logging

from model.generator import Generator
from model.generator_factory import GeneratorFactory

class Style(object):
    def __init__(self, name=""):
        self.name = name
        self.locked = "false" # TODO: fix to boolean & implement
        self.generators = []

    @staticmethod
    def default():
        s = Style("default style")
        g = Generator("bars")
        g.active = "true"
        s.generators.append(g)
        return s

    def get_active_generator(self):
        for g in self.generators:
            if g.active == "true": # TODO: fix to bool
                return g
        logging.info("# cannot find active generator")
        return None

    def _find_generator(self, name):
        for g in self.generators:
            if g.name == name: return g
        return None

    def set_active_generator(self, name):
        cur_gen = self.get_active_generator()
        g = self._find_generator(name)
        if not g:
            g = Generator(name)
            self.generators.append(g)
        g.active = "true"
        cur_gen.active = "false"

    def copy(self):
        s = Style()
        s.name = self.name
        s.locked = self.locked
        s.generators = []
        for g in self.generators:
            s.generators.append(g.copy())
        return s


def main():
    pass

if __name__ == "__main__":
    main()
