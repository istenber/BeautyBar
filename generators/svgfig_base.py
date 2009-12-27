import logging

from base import BaseGenerator

from lib.svgfig import *


class SvgFigGenerator(BaseGenerator):

    def __init__(self):
        self.rows = []
    
    def output(self):
        svg = SVG("svg")
        svg.append(self.get_defs())
        svg.append(self.get_elements())
        svg.attr["height"] = "200px"
        svg.attr["width"] = "300px"
        svg.attr["xmlns"] = "http://www.w3.org/2000/svg"
        svg.attr["xmlns:svg"] = "http://www.w3.org/2000/svg"
        svg.attr["xmlns:xlink"] = "http://www.w3.org/1999/xlink"
        return svg.standalone_xml()

    def set_range(self, min, max):
        self.min = min
        self.max = max

    def add_row(self, name, value, index=None):
        self.rows.append([name, value])

    def get_defs(self):
        raise Exception("not implemented")

    def get_elements(self):
        raise Exception("not implemented")
