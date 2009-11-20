#!/usr/bin/env python

import logging

from model.generator import Generator

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

def main():
    pass

if __name__ == "__main__":
    main()
