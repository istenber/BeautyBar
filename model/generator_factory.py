#!/usr/bin/env python

import os
import logging 

from singleton import Singleton

# TODO: move code to generators/base.py

generators_folder = "generators"

class Simple(object):
    def name(self):
        return "no name"

class GeneratorFactory(Singleton):

    def __init__(self):
        self.generators = []
        self._update()

    def _update(self):
        # files = os.listdir(generators_folder)
        # files = os.listdir(generators_folder)
        # files.sort()
        # TODO: houses disabled for now
        for generator in ["nature", "standard", "plain", "equalizer",
                          "shiny", "paper"]:
            #if file in skip_files: continue
            #if file.endswith(".py"):
            self.generators.append(self.get_generator(generator + ".py"))

    def get_generator(self, file):
        classname = file[:-3].capitalize()
        modulenames = ["generators." + file[:-3], file[:-3]]
        for modulename in modulenames:
            try:
                exec("from " + modulename + " import " + classname)
                return eval(classname)()
            except ImportError, error:
                logging.info("missing generator: " + modulename)
        return None # TODO: or skel generator?

    @classmethod
    def list(self):
        # raise Exception("inst: " + str(self.instance()))
        return self.instance().generators

def main():
    logging.getLogger().setLevel(logging.DEBUG)
    import sys
    sys.path = ["/home/sankari/dev/beautybar"] + sys.path
    print "sys.path: " + str(sys.path)
    print "\n"
    print "instance:   " + str(GeneratorFactory().instance())
    print "generators: " + str(GeneratorFactory().list())
    g = GeneratorFactory()
    print "generators: " + str(g.list())
    for one in g.list():
        print "-> " + str(one.get_ui_name())

if __name__ == "__main__":
    main()
