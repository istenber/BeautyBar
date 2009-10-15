#!/usr/bin/env python

class GuiInterface(object):
    """Abstract base class for all generators"""

    def __init__(self):
        if self.__class__ is GuiInterface:
            raise NotImplementedError

    def name(self):
        """Should return human readble name of generator"""
        return "no name"

    def attributes(self):
        """Should return list of all attributes that generator can take
        in human readble form"""
        return []

def usage(msg):
    import sys
    print "ERROR MSG: " + str(msg)
    print "usage: ./generators/gui_interface.py <filename.py>"        
    sys.exit(0)

def main():
    import sys
    import getopt
    try:
        opts, args = getopt.getopt(sys.argv[1:], "", [])
    except getopt.error:
        usage("extra args...")
    if not len(args) == 1:
        usage("provide exact one class to test")
    test_generator(args[0])

def test_generator(filename):
    if filename[:10] == "generators":
        filename = filename[11:]
    # print "filename = " + filename    
    classname = filename[:-3].capitalize()
    # import_cmd = "from generators." + filename[:-3] + " import " + classname
    import_cmd = "from " + filename[:-3] + " import " + classname
    try:
        exec(import_cmd)
    except ImportError:
        usage("import failed from \"" + filename + "\"")
    # print "import cmd = " + import_cmd
    # print "classname = " + classname
    g = eval(classname)()
    print ""
    print "GuiInterface of \"" + str(g.name()) + "\""
    print "---------------------------------------"
    for attr in g.attributes():
        print attr.name()
    print "---------------------------------------"

if __name__ == "__main__":
    main()
