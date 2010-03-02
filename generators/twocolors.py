import logging

from svgfig_base import SvgFigGenerator
from attributes.common import Color, Integer, Boolean

from lib.svgfig import *


class Twocolors(SvgFigGenerator):

    def __init__(self):
        SvgFigGenerator.__init__(self)
        self.color1 = "800000"
        self.color2 = "ffff00"
        self.ld = 7
        self.rd = 12
        self.has_grid = True
        self.dash_grid = True

    def get_elements(self):
        return SVG("g",
                   self.get_bg(),
                   self.get_grid(),
                   self.get_bars(),
                   self.get_titles())

    def get_bg(self):
        g = SVG("g")
        g.append(SVG("rect", x=0, y=0, width=300, height=170,
                     style="fill:#" + self.color1 + ";"))
        g.append(SVG("rect", x=10, y=5, width=280, height=160,
                     style="fill:#" + self.color2 + ";"))
        return g

    def get_grid(self):
        g = SVG("g")        
        if self.dash_grid:
            style = ("stroke:#" + self.color1 + ";stroke-width:1px;" +
                     "stroke-dasharray:1,2;stroke-dashoffset:0;")
        else:
            style = "stroke:#" + self.color1 + ";stroke-width:1px;"
        if self.has_grid:
            for i in range(0, 5):
                y = 5 + 32 * i
                g.append(SVG("path", d="M 0,%d L 300,%d" % (y, y),
                             style=style))
        return g

    def get_bars(self):
        g = SVG("g")
        w = 35 - self.ld - self.rd - 4
        for i in range(0, 6):
            x = 15 + 45 * i
            h = self.get_row_value(i) * 170
            g.append(SVG("rect", x=x+5, y=180-h, width=35, height=h,
                         style="fill:#" + self.color1 + ";"))
            g.append(SVG("rect", x=x+5+self.rd+2, y=180-h+2,
                         width=w, height=h-4,
                         style="fill:#" + self.color2 + ";"))
        return g

    def get_titles(self):
        g = SVG("g")
        style = "fill:#" + self.color1 + ";text-anchor:middle;"
        for i in range(0, 6):
            x = 37 + 45 * i
            name = self.get_row_name(i, max_len=6)
            g.append(Text(x, 190, name, font_size=12, style=style).SVG())
        return g

    def get_description(self):
        return "Simple chart with two main colors"

    def get_ui_name(self):
        return "Two Colors"

    def get_attributes(self):
        color1 = Color(self, "color1", "Color 1")
        color2 = Color(self, "color2", "Color 2")
        ld = Integer(self, "ld", "Bar left space", 2, 15, 7)
        rd = Integer(self, "rd", "Bar right space", 2, 15, 12)
        has_grid = Boolean(self, "has_grid", "Show grid")
        dash_grid = Boolean(self, "dash_grid", "Dashed grid lines")
        return [color1, color2, ld, rd, has_grid, dash_grid]

    def get_version(self):
        return 1
