#!/usr/bin/env python2.5

if __name__ == '__main__':
    import sys
    sys.path.append('/home/sankari/dev/beautybar')


from base import BaseGenerator
from lib.generator_calc import GeneratorCalc
from lib.svgfig import *


class SvgFigGenerator(BaseGenerator):
    """Base class for SvgFig based generators.

    Derived classes should implement get_elements method, and if
    want also get_defs method, and methods derived from GuiInterface.

    It will also provide interface to GeneratorCalc which contains
    helpers to set bars in correct places.

    Lets test that calcs are set correctly

       >>> class Gen(SvgFigGenerator):
       ...   def get_elements(self):       
       ...     self.v = self.get('edge')
       ...     return SVG('g')
       >>> g = Gen()
       >>> g.output()[:10]
       u'<?xml vers'
       >>> g.v
       12

    Shortcuts...

       >>> g.get('edge')
       12
       >>> g.left(0)
       23

    """

    def get(self, attr):
        if not hasattr(self, "calc"):
            self.calc = GeneratorCalc()
        return self.calc.get(attr)
    
    def left(self, index):
        if not hasattr(self, "calc"):
            self.calc = GeneratorCalc()
        return self.calc.left(index)

    def middle(self, index):
        if not hasattr(self, "calc"):
            self.calc = GeneratorCalc()
        return self.calc.middle(index)

    def output(self):
        svg = SVG("svg")
        if hasattr(self, "get_defs"):
            svg.append(self.get_defs())
        svg.append(self.get_elements())
        svg.attr["height"] = "200px"
        svg.attr["width"] = "300px"
        svg.attr["xmlns"] = "http://www.w3.org/2000/svg"
        svg.attr["xmlns:svg"] = "http://www.w3.org/2000/svg"
        svg.attr["xmlns:xlink"] = "http://www.w3.org/1999/xlink"
        return svg.standalone_xml()

    def get_elements(self):
        """Need to be implemented in derived classes."""
        raise Exception("not implemented")


if __name__ == '__main__':
    import doctest
    doctest.testmod()
