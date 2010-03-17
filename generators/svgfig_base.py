#!/usr/bin/env python2.5

if __name__ == '__main__':
    import sys
    import os
    sys.path.append(os.path.abspath(os.path.dirname('..')))


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
       ...     self.calc(edge_width = 15)
       ...     return SVG('g')
       >>> g = Gen()
       >>> for i in range(0, 3): g.add_row('a', 10)
       >>> g.output()[:10]
       u'<?xml vers'
       >>> g.calc.edge_width
       15
       >>> g.calc.left(0)
       37

    """

    def __init__(self):
        BaseGenerator.__init__(self)
        self.calc = GeneratorCalc()

    def output(self):
        svg = SVG("svg")
        self.calc.bar_count = self.get_row_count()
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
