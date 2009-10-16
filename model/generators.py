#!/usr/bin/env python

import os
from singleton import Singleton

skip_files = ["__init__.py", "gui_interface.py"]

class Simple(object):
    def name(self):
        return "no name"

class Generators(Singleton):
    __generators_path="generators"

    def __init__(self):
        self._update()

    def _update(self):    
        files = os.listdir(Generators.__generators_path)
        self.generators = []
        for file in files:
            if file in skip_files: continue
            if file.endswith(".py"):
                self.generators.append(self._get_generator(file))

    def _get_generator(self, filename):
        classname = filename[:-3].capitalize()
        # if not classname == "Bars": return Simple()
        icmd = "from generators." + filename[:-3] + " import " + classname
        # print "icmd: " + icmd
        try:
            exec(icmd)
        except ImportError, error:
            # TODO: remove this and simple class
            return Simple()
            import sys
            raise Exception("\n" + 
                            "msg      => " + str(error) + "\n" + 
                            "icmd     => " + icmd + "\n"
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
    print "instance:   " + str(Generators().instance())
    print "generators: " + str(Generators().list())
    g = Generators()
    print "generators: " + str(g.list())
    for one in g.list():
        print "-> " + str(one.name())

if __name__ == "__main__":
    main()
