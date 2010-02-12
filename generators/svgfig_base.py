import logging

from base import BaseGenerator

from lib.svgfig import *


class SvgFigGenerator(BaseGenerator):
    """Base class for SvgFig based generators.

    Derived classes should implement get_elements method, and if
    want also get_defs method. And of course methods derived from
    gui_interface. SvgFigGenerator sets self.min and self.max, and
    collects data to self.rows.
    """

    def __init__(self):
        self.rows = []
    
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

    def add_row(self, name, value, index=None):
        self.rows.append([name, value])

    def get_elements(self):
        """Need to be implemented in derived classes."""
        raise Exception("not implemented")
