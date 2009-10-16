#!/usr/bin/env python

import os
from singleton import Singleton

skip_files = ["__init__.py", "gui_interface.py"]

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
                self.generators.append(file[:-3])

    @classmethod
    def list(self):
        # raise Exception("inst: " + str(self.instance()))
        return self.instance().generators

def main():
    print "instance:   " + str(Generators().instance())
    print "generators: " + str(Generators().list())
    g = Generators()
    print "generators: " + str(g.list())

if __name__ == "__main__":
    main()
