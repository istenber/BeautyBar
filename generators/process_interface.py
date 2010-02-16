#!/usr/bin/env python

class ProcessInterface(object):
    """All chart processing should go through this interface."""

    def __init__(self):
        if self.__class__ is ProcessInterface:
            raise NotImplementedError

    def set_range(self, min, max):
        pass

    def set_attribute(self, attribute, value):
        setattr(self, attribute, value)

    def add_row(self, name, value, index=None):
        pass

    def output(self):
        return ""


def tester(name):

    def usage(msg=None):
        if msg is not None: print "ERROR MSG: " + str(msg)
        print "usage: ./diagrams/" + name + " <filename.py>"        
        sys.exit(0)

    # TODO: this should be default for all files?!
    import sys
    sys.path = ["/home/sankari/dev/beautybar"] + sys.path
    
    import getopt

    from model.generator_factory import GeneratorFactory
    from generators.attributes.attribute import Attribute, is_valid_attribute

    try:
        opts, args = getopt.getopt(sys.argv[1:], "", [])
    except getopt.error:
        usage("extra args...")
    if not len(args) == 1:
        usage()
    filename = args[0]
    if filename[:10] == "generators":
        filename = filename[11:]
    gf = GeneratorFactory().instance()
    diagram = gf.get_generator(filename)
    if diagram is None:
        usage("import failed from \"" + filename + "\"")
    return diagram

def main():
    import logging
    logging.getLogger().setLevel(logging.DEBUG)
    diagram = tester("process_interface.py")
    diagram.add_row("Ilpo", 28)
    diagram.add_row("Lasse", 24)
    diagram.add_row("Sanna", 27)
    diagram.add_row("Ilpo", 28)
    diagram.add_row("Lasse", 24)
    diagram.add_row("Very long title name", 27)
    diagram.set_range(0, 50)
    print diagram.output()

if __name__ == "__main__":
    main()
