import logging
import math
from random import Random as Rnd

from svgfig_base import SvgFigGenerator
from attributes.common import Choice, Integer, Color, Boolean

from lib.svgfig import *
from lib.utils import *


class Rocks(SvgFigGenerator):

    def __init__(self):
        SvgFigGenerator.__init__(self)
        self.color_set = 1
        self.rock_size = 12
        self.tcolor = "000000"
        self.has_ground = True
        self.gcolor = "008000"
        self.random = Rnd()
        self.random.seed(1000)

    def get_elements(self):
        self.calc(edge_width = 10,
                  bar_size = 90,
                  font_size = 13)
        return SVG("g",
                   self._get_ground(),
                   self._get_bars(),
                   self._get_names())

    def _my_rnd(self):
        return (self.random.random() - 0.5) * 3

    def _colors(self):
        c = [["ff0000", "00ff00", "0000ff",   # rainbow
              "ffff00", "00ffff", "ff00ff"],

             ["808080", "a9a9a9", "d3d3d3"],  # grey

             ["111111", "222222", "333333",   # dark
              "444444", "555555", "666666"],
             ]
        return c[self.color_set - 1]

    def _get_ground(self):
        g = SVG("g")
        if self.has_ground:
            g.append(SVG("rect", x=0, y=155, width=300,
                         height=15, style="fill:#%s;" % self.gcolor))
            g.append(SVG("rect", x=0, y=185, width=300,
                         height=15, style="fill:#%s;" % self.gcolor))
        return g

    def _get_names(self):
        names = SVG("g")
        tstyle = "fill:#%s;text-anchor:middle;font-weight:bold;" % self.tcolor
        for i in range(0, self.get_row_count()):
            n = "[" + self.get_row_name(i, max_len=7) + "]"
            t = Text(self.calc.middle(i), 182, n,
                     font_size = self.calc.font_size,
                     style = tstyle).SVG()
            names.append(t)
        return names

    def _get_one(self, x_base, width, val):
        g = SVG("g")
        size = self.rock_size # 10.0 # * (width / 30.0)
        logging.info("w: " + str(size))
        dy = 0.0
        last_dx = width * 1.0
        while dy < val:
            dx = 0.0
            while dx < last_dx - size:
                cr = int(math.floor(self.random.random() *
                                    len(self._colors()) + 0.5)) - 1
                style = ("stroke-width:1px;stroke:#000000;fill:#" +
                         self._colors()[cr] + ";")
                h = size + self._my_rnd()
                w = size + self._my_rnd()
                x0 = x_base + dx + self._my_rnd()
                x1 = x_base + dx + size + self._my_rnd()
                y0 = 160 - dy - size + self._my_rnd()
                y1 = 160 - dy + self._my_rnd()                
                xr = self._my_rnd()
                yr = self._my_rnd()
                d = ("M " + str(x0) + "," + str(y0) +
                     " L " + str(x1 + xr) + "," + str(y0) +
                     " L " + str(x1) + "," + str(y1 + yr) +
                     " L " + str(x0) + "," + str(y1) + " z")
                g.append(SVG("path", d = d, style = style))
                # rectange version
                # g.append(SVG("rect", height = h, width = w,
                #              x = x_base + dx, y = 160 - size - dy,
                #              style = style))
                dx += size
            last_dx = dx
            dy += size
            size -= 0.5
            x_base += 0.5
        return g

    def _get_bars(self):
        bars = SVG("g")
        for i in range(0, self.get_row_count()):
            x = self.calc.left(i)
            value = self.get_row_value(i) * 100.0
            bars.append(self._get_one(x, self.calc.bar_width, value))
        return bars

    def get_description(self):
        return "Rock piled top of each others"

    def get_ui_name(self):
        return "Rocks"

    def get_attributes(self):
        color_set = Choice(self, "color_set", "Color set",
                           ["Rainbow", "Grey", "Dark"])
        rock_size = Integer(self, "rock_size", "Rock size", 10, 20, 12)
        tcolor = Color(self, "tcolor", "Text color")
        has_ground = Boolean(self, "has_ground", "Show ground")
        gcolor = Color(self, "gcolor", "Ground color")
        return [color_set, rock_size, tcolor, has_ground, gcolor]

    def get_version(self):
        return 2
