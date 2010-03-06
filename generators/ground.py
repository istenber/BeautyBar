import logging

from svgfig_base import SvgFigGenerator
from attributes.common import Color, Boolean, Float

from lib.svgfig import *


# TODO: make common
class Rect(object):
    def __init__(self, x, y, width, height, style, rounding=10):
        self.style = style
        x0 = x
        x1 = x + rounding
        x2 = x + width - rounding
        x3 = x + width
        y0 = y
        y1 = y + rounding
        y2 = y + height - rounding
        y3 = y + height
        d = ("M %d,%d C %d,%d %d,%d %d,%d" % (x0, y1, x0, y0, x0, y0, x1, y0) +
             "L %d,%d C %d,%d %d,%d %d,%d" % (x2, y0, x3, y0, x3, y0, x3, y1) +
             "L %d,%d C %d,%d %d,%d %d,%d" % (x3, y2, x3, y3, x3, y3, x2, y3) +
             "L %d,%d C %d,%d %d,%d %d,%d" % (x1, y3, x0, y3, x0, y3, x0, y2) +
             "L %d,%d z" % (x0, y1))
        self.d = d

    def SVG(self):
        return SVG("path", d=self.d, style=self.style)


class Ground(SvgFigGenerator):

    def __init__(self):
        SvgFigGenerator.__init__(self)
        self.gcolor = "ff0000"
        self.bcolor = "00eeff"
        self.tcolor = "ffff00"
        self.has_bg = True
        self.has_text = True
        self.shadow_size = 2.0

    def get_defs(self):
        defs = SVG("defs", id="defs")
        sh = SVG("feGaussianBlur", stdDeviation=self.shadow_size)
        defs.append(SVG("filter", sh, id="shadow"))
        return defs

    def get_elements(self):
        self.calc(edge_width=20,
                  bar_size=60)
        return SVG("g",
                   self.get_bg(),
                   self.get_shadows(),
                   self.get_bars(),
                   self.get_names())

    def get_bg(self):
        g = SVG("g")
        if self.has_bg:            
            sbg = "fill:#%s;" % self.bcolor
            ssh = "fill:#000000;filter:url(#shadow);"
            g.append(Rect(x=10, y=10, width=280, height=160, style=ssh).SVG())
            g.append(Rect(x=10, y=10, width=280, height=160, style=sbg).SVG())
        return g

    def get_names(self):
        g = SVG("g")
        s = "fill:#%s;" % self.gcolor
        g.append(Rect(x=15, y=160, width=270, height=30, style=s).SVG())
        if self.has_text:
            ts = "fill:#%s;text-anchor:middle;font-weight:bold;" % self.tcolor
            fs = self.calc.font_size
            for i in range(0, self.get_row_count()):
                x = self.calc.middle(i)
                name = self.get_row_name(i)
                g.append(Text(x, 180, name, font_size=fs, style=ts).SVG())
        return g

    def get_bars(self):
        g = SVG("g")
        s = "fill:#%s;" % self.gcolor
        w = self.calc.bar_width
        for i in range(0, self.get_row_count()):
            x = self.calc.left(i)
            h = self.get_row_value(i) * 150 + 5
            g.append(Rect(x=x, y=165-h, height=h, width=w, style=s).SVG())
        return g

    def get_shadows(self):
        g = SVG("g")
        s = "fill:#000000;filter:url(#shadow);"
        w = self.calc.bar_width
        for i in range(0, self.get_row_count()):
            x = self.calc.left(i)
            h = self.get_row_value(i) * 150 + 5
            g.append(Rect(x=x, y=165-h, height=h, width=w, style=s).SVG())
        g.append(Rect(x=15, y=160, width=270, height=30, style=s).SVG())
        return g

    def get_description(self):
        return "Bars rise from ground nicely"

    def get_ui_name(self):
        return "From ground bars rise"

    def get_attributes(self):
        shadow_size = Float(self, "shadow_size", "Shadow size", 1.0, 3.0)
        gcolor = Color(self, "gcolor", "Ground Color")
        has_bg = Boolean(self, "has_bg", "Background?")
        bcolor = Color(self, "bcolor", "Background Color")
        has_text = Boolean(self, "has_text", "Text?")
        tcolor = Color(self, "tcolor", "Text Color")
        return [shadow_size, gcolor, has_bg, bcolor, has_text, tcolor]

    def get_version(self):
        return 2
