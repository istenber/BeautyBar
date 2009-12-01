#!/usr/bin/env python

import logging

from model.generator import Generator
from model.generator_factory import GeneratorFactory


class Style(object):

    def __init__(self, name=""):
        self.name = name
        self.locked = False
        self.generators = []

    @staticmethod
    def default():
        s = Style("default style")
        g = Generator("standard")
        g.active = True
        s.generators.append(g)
        return s

    def get_active_generator(self):
        for g in self.generators:
            if g.active: return g
        logging.info("# cannot find active generator")
        return None

    def _find_generator(self, name):
        for g in self.generators:
            if g.name == name: return g
        return None

    def set_active_generator(self, name):
        old_gen = self.get_active_generator()
        if old_gen.name == name:
            return
        g = self._find_generator(name)
        if not g:
            g = Generator(name)
            self.generators.append(g)
        g.active = True
        old_gen.active = False

    def copy(self):
        s = Style()
        s.name = self.name
        s.locked = False
        s.generators = []
        for g in self.generators:
            s.generators.append(g.copy())
        return s


def main():
    pass

if __name__ == "__main__":
    main()
