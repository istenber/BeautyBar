#!/usr/bin/env python

import os

class Generators(object):
    __instance = None
    __generators_path="generators"

    def __init__(self):
        self._update()

    def _update(self):    
        files = os.listdir(Generators.__generators_path)
        self.generators = []
        for file in files:
            if file == "__init__.py": continue
            if file.endswith(".py"):
                self.generators.append(file[:-3])

    @staticmethod
    def _get_instance():
        if Generators.__instance is None:
            Generators.__instance = Generators()
        return Generators.__instance

    @staticmethod
    def list():
        return Generators._get_instance().generators

def main():
    g = Generators()
    print "generators: " + str(g.list())

if __name__ == "__main__":
    main()
