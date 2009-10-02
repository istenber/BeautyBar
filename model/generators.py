#!/usr/bin/env python

import os

generators_path="generators"

class Generators(object):

    def __init__(self):
        self._update()
    def _update(self):    
        files = os.listdir(generators_path)
        self.generators = []
        for file in files:
            if file == "__init__.py": continue
            if file.endswith(".py"):
                self.generators.append(file[:-3])
    def list(self):
        return self.generators

def main():
    g = Generators()
    print "generators: " + str(g.list())

if __name__ == "__main__":
    main()
