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
        s = Style()
        g = Generator("bars")
        g.active = "true"
        s.generators.append(g)
        return s

def main():
    pass

if __name__ == "__main__":
    main()
