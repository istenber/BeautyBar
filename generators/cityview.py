import logging
import random

from svgfig_base import SvgFigGenerator
from attributes.common import Color, Boolean, Choice

from lib.svgfig import *


class Cityview(SvgFigGenerator):

    def __init__(self):
        SvgFigGenerator.__init__(self)
        self.color = "000000"
        # TODO: random seed and other attributes
        random.seed(300)

    def get_defs(self):
        defs = SVG("defs", id="defs")
        return defs

    def get_elements(self):
        return SVG("g",
                   self.get_back_bars(),
                   self.get_bars(),
                   self.get_front_bars(),
                   self.get_ground())

    def get_ground(self):
        g = SVG("g")
        g.append(SVG("rect", x=0, y=149, width=300, height=2,
                     style="fill:#cccccc"))
        g.append(SVG("rect", x=0, y=49, width=300, height=2,
                     style="fill:#888888"))
        g.append(SVG("rect", x=0, y=151, width=300, height=2,
                     style="fill:#888888"))
        g.append(SVG("rect", x=0, y=51, width=300, height=2,
                     style="fill:#cccccc"))
        return g
                 
    def random_color(self):
        # TODO: more colors
        colors = ['91ff91', 'ffffb9', 'f4c7c4', 'b9ffff']
        r = int(random.random() * len(colors))
        return "fill:#" + colors[r] + ";"

    def get_front_bars(self):
        bars = SVG("g")
        for i in range(0, 5):
            m = 100 * min(self.get_row_value(i), self.get_row_value(i+1)) - 20
            if m < 0: continue
            h = int(0.5 * m + 0.5 * random.random() * m)
            # logging.info("front(" + str(i) + "):" + str(h))            
            # 300 = 0 + 60 + 0, 5 + 50 + 5
            x = 5 + 60 * i
            bar = SVG("rect", x=x, height=h, style=self.random_color(),
                      width=50, y=150-h+1)
            bars.append(bar)
        return bars

    def get_back_bars(self):
        bars = SVG("g")
        for i in range(0, 5):
            h = int(random.random() * 100)
            # logging.info("back(" + str(i) + "):" + str(h))
            # 300 = 0 + 60 + 0, 5 + 50 + 5
            x = 32 + 47 * i
            bar = SVG("rect", x=x, height=h, style=self.random_color(),
                      width=41, y=150-h+1)
            bars.append(bar)
        return bars

    def get_bars(self):
        bars = SVG("g")
        tsw = "fill:#ffffff; font-weight: bold; text-anchor:middle;"
        tsb = "fill:#" + self.color + "; font-weight: bold; text-anchor:middle;"
        color = "fill:#" + self.color + ";"
        for i in range(0, self.get_row_count()):
            h = self.get_row_value(i) * 100
            # 300 = 9 + 282 / 6 + 9 -> 47 = 6 + 35 + 6... 9+6 = 15
            x = 15 + 47 * i
            bar = SVG("rect", x=x, height=h, style=color,
                      width=35, y=150-h)
            bars.append(bar)
            name = self.get_row_name(i, max_len=7)
            if h < 20:
                t = Text(x+17, 148-h, name, font_size=8, style=tsb).SVG()
            else:
                t = Text(x+17, 162-h, name, font_size=8, style=tsw).SVG()
            bars.append(t)
        return bars

    def get_description(self):
        return "Looks like a city - or not"

    def get_ui_name(self):
        return "City View"

    def get_attributes(self):
        color = Color(self, "color", "Color")
        return [color]

    def get_rating(self):
        return 1

    def get_version(self):
        return 2
