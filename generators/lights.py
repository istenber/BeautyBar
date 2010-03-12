import logging

from svgfig_base import SvgFigGenerator
from attributes.common import Integer, Color, Boolean, Choice

from lib.svgfig import *


class Lights(SvgFigGenerator):

    def __init__(self):
        SvgFigGenerator.__init__(self)
        self.has_singlebg = False
        self.bgcolor = "cccccc"
        self.gsize = 33
        self.ysize = 33
        self.rsize = 33
        self.y0 = 20

    def normalize_colors(self):
        tot = (self.gsize + self.ysize + self.rsize) / 100.0
        self.gsize = int(self.gsize / tot)
        self.ysize = int(self.ysize / tot)
        self.rsize = int(self.rsize / tot)
 
    def get_elements(self):
        self.calc(edge_width=10,
                  bar_size=95,
                  font_size=10)
        self.normalize_colors()
        return SVG("g",
                   self.get_bg(),
                   self.get_bars(),
                   self.get_names())

    def get_bg(self):
        g = SVG("g")
        f = (170 - self.y0) / 100.0
        gs = int(self.gsize * f)
        ys = int(self.ysize * f)
        rs = 170 - self.y0 - gs - ys
        # rs = int(self.rsize * f)
        g.append(SVG("rect", x=0, y=0, width=300, height=200,
                     style="fill:#000000;"))
        if self.has_singlebg:
            g.append(SVG("rect", x=3, y=self.y0, width=294, height=170-self.y0,
                         style="fill:#%s;" % self.bgcolor))
        else:
            g.append(SVG("rect", x=3, y=self.y0, width=294, height=gs+2,
                         style="fill:#91ff91;"))
            g.append(SVG("rect", x=3, y=self.y0+gs, width=294, height=ys+2,
                         style="fill:#ffff91;"))
            g.append(SVG("rect", x=3, y=self.y0+gs+ys, width=294, height=rs,
                         style="fill:#ff9191;"))
        return g

    def get_color(self, val, dark=False):
        if val <= (self.rsize / 100.0):
            if dark: return "800000"
            else: return "ff0000"
        if val <= ((self.rsize + self.ysize) / 100.0):
            if dark: return "808000"
            else: return "ffff00"
        if dark: return "008000"
        else: return "00ff00"

    def get_bars(self):
        g = SVG("g")
        for i in range(0, self.get_row_count()):
            x = self.calc.left(i)
            h = int(self.get_row_value(i) * (170.0 - self.y0))
            w = self.calc.bar_width
            bstyle = "fill:#%s;" % self.get_color(self.get_row_value(i),
                                                  dark=True)
            bgb = SVG("rect", x=x, y=170-h, width=w, height=h, style=bstyle)
            g.append(bgb)
            bstyle = "fill:#%s;" % self.get_color(self.get_row_value(i))
            w = (self.calc.bar_width * 0.7)
            n = (self.calc.bar_width - w) / 2
            yn = min(h, n)
            bar = SVG("rect", x=x+n, y=170-h+yn, width=w,
                      height=h+20-yn, style=bstyle)
            g.append(bar)
        return g

    def get_names(self):
        g = SVG("g")
        ts0 = "font-weight:bold;text-anchor:middle;"
        for i in range(0, self.get_row_count()):
            x = self.calc.left(i)
            w = self.calc.bar_width
            v = self.get_row_value(i)
            ts = ts0 + "fill:#%s;" % self.get_color(v, dark=True)
            g.append(SVG("rect", x=x, y=175, width=w, height=15,
                         style="fill:#%s;" % self.get_color(v)))
            xm = self.calc.middle(i)
            name = self.get_row_name(i, max_len=6)
            text = Text(xm, 185, name, font_size=self.calc.font_size, style=ts)
            g.append(text.SVG())
        return g

    def get_description(self):
        return "Color show how good status is"

    def get_ui_name(self):
        return "Traffic Lights"

    def get_attributes(self):
        has_singlebg = Boolean(self, "has_singlebg", "Single color bg")
        bgcolor = Color(self, "bgcolor", "Background color")
        gsize = Integer(self, "gsize", "Green relative size", 0, 100, 33)
        ysize = Integer(self, "ysize", "Yellow relative size", 0, 100, 33)
        rsize = Integer(self, "rsize", "Red relative size", 0, 100, 33)
        y0 = Integer(self, "y0", "Top space size", 0, 40, 20)
        return [has_singlebg, bgcolor, gsize, ysize, rsize, y0]

    def get_version(self):
        return 2
