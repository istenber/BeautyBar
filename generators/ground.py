import logging

from svgfig_base import SvgFigGenerator
from attributes.common import Color, Boolean, Float

from lib.svgfig import *


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
            g.append(RoundedRect(x1=10, y1=10, x2=290, y2=170, r=10,
                                 style=ssh).SVG())
            g.append(RoundedRect(x1=10, y1=10, x2=290, y2=170, r=10,
                                 style=sbg).SVG())
        return g

    def get_names(self):
        g = SVG("g")
        s = "fill:#%s;" % self.gcolor
        g.append(RoundedRect(x1=15, y1=160, x2=285, y2=190, r=10,
                             style=s).SVG())
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
            g.append(RoundedRect(x1=x, y1=165-h, x2=x+w, y2=165, r=10,
                                 style=s).SVG())
        return g

    def get_shadows(self):
        g = SVG("g")
        s = "fill:#000000;filter:url(#shadow);"
        w = self.calc.bar_width
        for i in range(0, self.get_row_count()):
            x = self.calc.left(i)
            h = self.get_row_value(i) * 150 + 5
            g.append(RoundedRect(x1=x, y1=165-h, x2=x+w, y2=165, r=10,
                                 style=s).SVG())
        g.append(RoundedRect(x1=15, y1=160, x2=285, y2=190, r=10,
                             trans="x/2., y/2.",
                             style=s).SVG())
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
