import logging
import random

from svgfig_base import SvgFigGenerator
from attributes.common import Color, Title, Boolean
from lib.number_scaler import NumberScaler

from lib.svgfig import *


def _rounder(n):
    return int(round(n, -len(str(int(n))) + 1))


class Weights(SvgFigGenerator):

    def __init__(self):
        SvgFigGenerator.__init__(self)
        self.has_random = True
        self.fcolor = "cccccc"
        self.scolor = "0000ff"
        self.ncolor = "00ff00"
        self.lcolor = "ff0000"
        random.seed(20)

    def count_sizes(self):        
        self.small = _rounder((self.max - self.min) / 24.0)
        self.normal = self.small * 2
        self.large = self.normal * 2

    def get_elements(self):
        self.calc(edge_width=20,
                  bar_size=70,
                  font_size=13)
        self.field_style = ("fill:#" + self.fcolor + ";stroke:#000000;"
                            "stroke-width:2px;stroke-linejoin:round;")
        self.count_sizes()
        return SVG("g",
                   self.get_info_field(),
                   self.get_name_field(),
                   self.get_weights())

    def get_weight(self, x, y, color, height, move):
        if move and self.has_random:
            x = x - 3 + int(random.random() * 6)
            y = y - 1 + int(random.random() * 2)
        return SVG("rect", x=x, y=y, width=self.calc.bar_width,
                   height=height, style="fill:#" + color + ";")

    def get_large(self, x, y, move=True):
        return self.get_weight(x, y, self.lcolor, 13, move)

    def get_normal(self, x, y, move=True):
        return self.get_weight(x, y, self.ncolor, 8, move)

    def get_small(self, x, y, move=True):
        return self.get_weight(x, y, self.scolor, 5, move)

    def get_info_field(self):
        g = SVG("g", transform="scale(0.5, 0.5)")
        g.append(SVG("rect", x=10, y=10, height=70, width=100,
                     style=self.field_style))
        g.append(self.get_small(20, 15+8, move=False))
        g.append(self.get_normal(20, 35+5, move=False))
        g.append(self.get_large(20, 55, move=False))
        g.append(Text(60, 30, NumberScaler().scale(self.small),
                      font_size=15, style="fill:#000000;").SVG())
        g.append(Text(60, 50, NumberScaler().scale(self.normal),
                      font_size=15, style="fill:#000000;").SVG())
        g.append(Text(60, 70, NumberScaler().scale(self.large),
                      font_size=15, style="fill:#000000;").SVG())
        return g

    def get_name_field(self):
        g = SVG("g")
        g.append(SVG("rect", x=2, y=168, height=30, width=296,
                     style=self.field_style))
        text_style="fill:#000000;text-anchor:middle;"
        fs = self.calc.font_size
        for i in range(0, self.get_row_count()):
            name = self.get_row_name(i, max_len=6)
            x = self.calc.middle(i)
            g.append(Text(x, 185, name, font_size=fs, style=text_style).SVG())
        return g

    def get_weights(self):
        g = SVG("g")
        for i in range(0, self.get_row_count()):
            xm = self.calc.middle(i) - 2
            g.append(SVG("rect", x=xm, y=50, width=4, height=118,
                         style="fill:#000000;stroke:none"))
            v = self.rows[i][1] - self.min
            y0 = 160
            x = self.calc.left(i)
            while v >= self.large:
                y0 -= 15
                g.append(self.get_large(x, y0))
                v -= self.large
            while v >= self.normal:
                y0 -= 10
                g.append(self.get_normal(x, y0))
                v -= self.normal
            while v >= self.small:
                y0 -= 7
                g.append(self.get_small(x, y0))
                v -= self.small
        return g

    def get_description(self):
        return "Chart for athletes"

    def get_ui_name(self):
        return "Weight lifting"

    def get_attributes(self):
        has_random = Boolean(self, "has_random", "Weights have random move")
        fcolor = Color(self, "fcolor", "Field Color")
        title = Title(self, "Weight Colors")
        scolor = Color(self, "scolor", "Small")
        ncolor = Color(self, "ncolor", "Average")
        lcolor = Color(self, "lcolor", "Large")
        return [has_random, fcolor, title, scolor, ncolor, lcolor]

    def get_version(self):
        return 2
