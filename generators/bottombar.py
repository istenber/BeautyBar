import logging

from svgfig_base import SvgFigGenerator
from attributes.common import Color, Integer

from lib.svgfig import *


class Bottombar(SvgFigGenerator):

    def __init__(self):
        SvgFigGenerator.__init__(self)
        self.color = "008000"
        self.font_size = 12

    def get_elements(self):
        return SVG("g", 
                   self.get_bottom_bar(),
                   self.get_grid(),
                   self.get_bars())

    def get_bottom_bar(self):
        bottom_bar = SVG("g")
        bottom_bar.append(SVG("rect", x=0, y=170, width=300, height=30,
                              style="fill:#000000"))
        text_style = "fill:#" + self.color + "; text-anchor:middle;"
        for i in range(0, 6):
            name = self.get_row_name(i, max_len=6)
            x = 25 + i * 50
            t = Text(x, 190, name, font_size=self.font_size,
                     style=text_style).SVG()
            bottom_bar.append(t)
        return bottom_bar

    def get_grid(self):
        grid = SVG("g")
        for i in range(1, 6):
            y = 170 - 30 * i
            grid.append(SVG("rect", x=5, y=y, width=290, height=2,
                         style="fill:#eeeeee;"))
        return grid

    def get_bars(self):
        bars = SVG("g")
        shadow_style = "fill:#000000;"
        bar_style = "fill:#" + self.color + ";"
        for i in range(0, 6):
            h = self.get_row_value(i) * 160
            sh = max(h - 5, 0)
            x = 10 + i * 50
            shadow = SVG("rect", x=x-1, y=170-sh, width=30, height=sh,
                         style=shadow_style)
            bar = SVG("rect", x=x+1, y=170-h, width=30, height=h,
                      style=bar_style)
            bars.append(shadow)            
            bars.append(bar)
        return bars

    def get_description(self):
        return "Bottom bar with titles"

    def get_ui_name(self):
        return "Bottom Bar"

    def get_attributes(self):
        color = Color(self, "color", "Color")
        font_size = Integer(self, "font_size", "Font Size", 8, 17, 12)
        return [color, font_size]
