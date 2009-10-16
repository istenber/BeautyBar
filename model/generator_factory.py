#!/usr/bin/env python

import os
from singleton import Singleton

skip_files = ["__init__.py", "gui_interface.py"]
generators_folder = "generators"

class Simple(object):
    def name(self):
        return "no name"

class GeneratorFactory(Singleton):

    def __init__(self):
        self._update()

    def _update(self):    
        files = os.listdir(generators_folder)
        self.generators = []
        for file in files:
            if file in skip_files: continue
            if file.endswith(".py"):
                self.generators.append(self._get_generator(file))

    def _get_generator(self, file):
        classname = file[:-3].capitalize()
        modulename = "generators." + file[:-3]
        # if not classname == "Bars": return Simple()
        try:
            exec("from " + modulename + " import " + classname)
        except ImportError, error:
            # TODO: remove this and simple class
            # return Simple()
            import sys
            raise Exception("\n" + 
                            "msg      => " + str(error) + "\n" + 
                            "sys.path => " + str(sys.path) + "\n")
        return eval(classname)()

    @classmethod
    def list(self):
        # raise Exception("inst: " + str(self.instance()))
        return self.instance().generators

def main():
    import sys
    sys.path = ["/home/ippe/dev/beautybar"] + sys.path
    print "sys.path: " + str(sys.path)
    print "\n"
    print "instance:   " + str(GeneratorFactory().instance())
    print "generators: " + str(GeneratorFactory().list())
    g = GeneratorFactory()
    print "generators: " + str(g.list())
    for one in g.list():
        print "-> " + str(one.name())

if __name__ == "__main__":
    main()
