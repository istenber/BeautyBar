import logging

from lib.svgfig import *
from svgfig_base import SvgFigGenerator
from attributes.common import Color, Boolean
from dots import CommonAttributesBase


class Semiwave(SvgFigGenerator, CommonAttributesBase):

    def __init__(self):
        SvgFigGenerator.__init__(self)
        CommonAttributesBase.__init__(self)
        self.from_edge = False

    def get_elements(self):
        self.calc(edge_width = 10,
                  bar_size = 60,
                  font_size = 12)
        return SVG("g",
                   self.get_lines())

    def get_lines(self):
        g = SVG("g")
        # w = self.calc.bar_width - self.ld - self.rd - 4
        s = ("fill:none;stroke-width:5px;stroke-linejoin:round;" + 
             "stroke-linecap:round;stroke:#%s;" % self.color)
        if self.from_edge:
            x0 = 0
        else:
            x0 = 10
        y0 = 170
        sp = 8
        yn = 30
        for i in range(0, self.get_row_count()):
            if self.get_row_value(i) < 0.1: continue
            x1 = self.calc.left(i)
            x2 = x1 + self.calc.bar_width
            h = y0 - self.get_row_value(i) * (y0 - yn)
            g.append(SVG("path",
                         d = (" M %s,%s L %s,%s" % (x0, y0, x1, y0) +
                              " L %s,%s L %s,%s" % (x1, h, x2, h)),
                         style = s))
            g.append(SVG("path",
                         d = (" M %s,%s L %s,%s" % (x1+sp, h+sp, x2, h+sp) +
                              " L %s,%s" % (x2, y0)),
                         style = s))
            x0 = x2
        if self.from_edge:
            x1 = 300
        else:
            x1 = 290
        g.append(SVG("path",
                     d = "M %s,%s L %s,%s" % (x0, y0, x1, y0),
                     style = s))
        return g

    def get_description(self):
        return "I feel seasick, should I?"

    def get_ui_name(self):
        return "Semi wave"

    def get_attributes(self):
        return []

    def get_version(self):
        return 2
