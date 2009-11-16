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

    # TODO: rename x_name with something nice
    def x_name(self):
        return self.__class__.__name__.lower()

    def __str__(self):
        out = ("\nGuiInterface of \"" + self.name() + "\" (" + 
               self.x_name() + ")\n" +
               "---------------------------------------\n")
        for attr in self.attributes():
            out += attr.name() + "\n"
        out += "---------------------------------------\n"
        return out


def main():

    def usage(msg):
        print "ERROR MSG: " + str(msg)
        print "usage: ./generators/gui_interface.py <filename.py>"        
        sys.exit(0)

    def have_required_field(generator, field):
        try:
            f = getattr(generator, field)
        except AttributeError, er:
            print "# missing field " + field
            return False
        if type(f) is types.MethodType: return True
        return False

    def generator_is_valid(generator):
        ok = True
        required_fields = ["name", "x_name", "attributes"]
        for f in required_fields:
            ok &= have_required_field(generator, f)
        return ok

    # TODO: this should be default for all files?!
    import sys
    sys.path = ["/home/sankari/dev/beautybar"] + sys.path

    import types
    import getopt
    from model.generator_factory import GeneratorFactory
    try:
        opts, args = getopt.getopt(sys.argv[1:], "", [])
    except getopt.error:
        usage("extra args...")
    if not len(args) == 1:
        usage("provide exact one class to test")
    filename = args[0]
    if filename[:10] == "generators":
        filename = filename[11:]
    gf = GeneratorFactory().instance()
    generator = gf.get_generator(filename)
    if generator is None:
        usage("import failed from \"" + filename + "\"")        
    print generator
    if generator_is_valid(generator):
        print generator.name() + " is valid"
    else:
        print generator.name() + " is invalid"

if __name__ == "__main__":
    main()
