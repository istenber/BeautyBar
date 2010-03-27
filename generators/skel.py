import logging

from lib.svgfig import *
from svgfig_base import SvgFigGenerator
from attributes.common import Color, Boolean


class Skel(SvgFigGenerator):

    def __init__(self):
        SvgFigGenerator.__init__(self)
        # TODO: set default values
        self.color = "ff0000"
        self.has_x = True

    # TODO: add definitions here
    def get_defs(self):
        return SVG("defs")

    # TODO: add elements here
    def get_elements(self):
        # set values to calculations
        self.calc(edge_width = 10,
                  bar_size = 80,
                  font_size = 12)
        return SVG("g",
                   self.get_bars(),
                   self.get_titles())

    # TODO: add bar generation
    def get_bars(self):
        g = SVG("g")
        if self.has_x:
            # TODO: do something?
            pass
        for i in range(0, self.get_row_count()):
            x = self.calc.left(i)
            h = self.get_row_value(i) * 170
            g.append(SVG("rect",
                         x = x,
                         y = 180-h,
                         width = self.calc.bar_width,
                         height = h,
                         style = "fill:#%s;" % self.color))
        return g

    # TODO: add title generation
    def get_titles(self):
        g = SVG("g")
        style = "fill:#%s;text-anchor:middle;" % "000000"
        fs = self.calc.font_size
        for i in range(0, self.get_row_count()):
            x = self.calc.middle(i)
            name = self.get_row_name(i, max_len=6)
            g.append(Text(x, 190, name, font_size=fs, style=style).SVG())
        return g

    # TODO: fill
    def get_description(self):
        return ""

    # TODO: fill
    def get_ui_name(self):
        return ""

    # TODO: add attributes
    def get_attributes(self):
        color = Color(self, "color", "Color")
        has_x = Boolean(self, "has_x", "Has x?")
        return [color, has_x]

    def get_version(self):
        return 2
