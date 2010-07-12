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


def precalc_bar_areas(generator, h, h0):
    """
    h  = height of bar
    h0 = distance from top
    """
    m = []
    for i in range(0, generator.get_row_count()):
        x0 = generator.calc.left(i)
        x1 = x0 + generator.calc.bar_width
        y0 = h0 + h - generator.get_row_value(i) * h
        y1 = h0 + h
        bar = (x0, y0, x1, y1)
        m.append(bar)
    return m

def in_limits(areas, x, y):
    for (x0, y0, x1, y1) in areas:
        if x > x0 and x < x1 and y > y0 and y < y1:
            return True
    return False


class Dots(SvgFigGenerator, CommonAttributesBase):

    def __init__(self):
        SvgFigGenerator.__init__(self)
        CommonAttributesBase.__init__(self)
        self.has_x = True
        self.dots_x = 30
        self.dots_y = 20
        self.big_dot = 4
        self.small_dot = 1

    def get_elements(self):
        self.calc(edge_width = 10,
                  bar_size = 60,
                  font_size = 12)
        self.areas = precalc_bar_areas(self, 170, 10)
        return SVG("g",
                   self.get_dots())

    def get_dots(self):
        g = SVG("g")
        style_a = ("fill:none;stroke-width:%spx;stroke:#%s;" %
                   (self.big_dot, self.color))
        style_b = ("fill:none;stroke-width:%spx;stroke:#%s;" %
                   (self.small_dot, self.color))
        # xplus = int(300 / self.dots_x)
        # yplus = int(200 / self.dots_y)
        # xp2 = int(xplus / 2)
        # yp2 = int(yplus / 2)
        xplus = 300.0 / self.dots_x
        yplus = 200.0 / self.dots_y
        xp2 = xplus / 2.0
        yp2 = yplus / 2.0
        for xi in range(0, self.dots_x):
            for yi in range(0, self.dots_y):
                x = xi * xplus + xp2
                y = yi * yplus + yp2
                if in_limits(self.areas, x, y):
                    style = style_a
                else:
                    style = style_b
                g.append(SVG("rect",
                             x = int(x) - 1,
                             y = int(y) - 1,
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
