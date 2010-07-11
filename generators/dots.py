import logging

from lib.svgfig import *
from svgfig_base import SvgFigGenerator
from attributes.common import Color, Boolean


# TODO: by this way "common attributes" will be different for all generators
#       not common in other words
class CommonAttributesBase(object):

    def __init__(self):
        self.color = "000000"
        self.bgcolor = "ffffff"

    def get_common_attributes(self):
        color = Color(self, "color", "Color")
        bgcolor = Color(self, "bgcolor", "Background Color")
        return [color, bgcolor]


class Dots(SvgFigGenerator, CommonAttributesBase):

    def __init__(self):
        SvgFigGenerator.__init__(self)
        CommonAttributesBase.__init__(self)
        self.has_x = True

    def get_elements(self):
        self.calc(edge_width = 10,
                  bar_size = 60,
                  font_size = 12)
        return SVG("g",
                   self.get_dots())

    def in_limits(self, x, y):
        for i in range(0, self.get_row_count()):
            x0 = self.calc.left(i)
            x1 = x0 + self.calc.bar_width
            y0 = self.get_row_value(i) * 170
            y1 = 170
            if x > x0 and x < x1 and y > y0 and y < y1:
                return True
        return False

    def get_dots(self):
        g = SVG("g")
        style_a = "fill:none;stroke-width:5px;stroke:#%s;" % self.color
        style_b = "fill:none;stroke-width:1px;stroke:#%s;" % self.color
        for xi in range(0, 30):
            for yi in range(0, 20):
                x = xi * 10 + 5 - 1
                y = yi * 10 + 5 - 1
                if self.in_limits(x, y):
                    style = style_a
                else:
                    style = style_b
                g.append(SVG("rect",
                             x = x,
                             y = y,
                             width = 2,
                             height = 2,
                             style = style))
        return g

    def get_description(self):
        return "Dots are geeky and nice"

    def get_ui_name(self):
        return "Dots"

    # TODO:
    def get_attributes(self):
        has_x = Boolean(self, "has_x", "Has x?")
        # TODO: get_common_attributes should not be called here!!!
        return [has_x] + self.get_common_attributes()

    def get_version(self):
        return 2
