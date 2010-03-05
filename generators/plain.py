import logging

from svgfig_base import SvgFigGenerator
from attributes.common import Color, Boolean

from lib.svgfig import *


class Plain(SvgFigGenerator):

    def __init__(self):
        SvgFigGenerator.__init__(self)
        self.color = "ffbbbb"
        self.has_text = False

    def get_elements(self):
        self.calc(edge_width = 35,
                  bar_size = 75)
        return SVG("g", 
                   self._get_background(),
                   self._get_bars())

    def _get_background(self):
        lines = SVG("g")
        for pos in range(0, 7):
            # 60 -- 140
            y = 70 + 10*pos
            line = SVG("path", d="M 10," + str(y) + " L 290," + str(y),
                       style="stroke:#" + self.color + ";stroke-width:2;")
            lines.append(line)
        bg = SVG("g",
                 lines,
                 SVG("rect", x=0, y=0, width=300, height=50,
                     style="fill:#" + self.color + ";"),
                 SVG("rect", x=0, y=150, width=300, height=50,
                     style="fill:#" + self.color + ";"),
                 SVG("rect", x=30, y=10, width=240, height=180,
                     style="fill:#ffffff;stroke:#" + self.color + ";"),
                 SVG("path", d="M 0, 165 L 300,165",
                     style="stroke:#" + self.color + ";stroke-width:2;"))
        return bg

    def _get_bars(self):
        bars = SVG("g")
        bar_width=self.calc.bar_width
        bstyle = "fill:#" + self.color + ";"
        tstyle = "fill:#" + self.color + "; text-anchor:middle;"
        fs = self.calc.font_size
        for index in range(0, self.get_row_count()):
            name = self.get_row_name(index, max_len=6)
            value = self.get_row_value(index) * 135
            x = self.calc.left(index)
            xm = self.calc.middle(index)
            pos = 165-value
            bar = SVG("rect", id="bar_" + name, width=bar_width, x=x,
                      y=pos, height=value, style = bstyle)
            if(self.has_text):
                t = Text(xm, 180, name, font_size=fs, style=tstyle).SVG()
                bars.append(t)
            bars.append(bar)
        return bars

    def get_description(self):
        return "Very simple and plain bar diagram"

    def get_ui_name(self):
        return "Plain"

    def get_attributes(self):
        color = Color(self, "color", "Color")
        has_text = Boolean(self, "has_text", "Show titles")
        return [color, has_text]

    def get_version(self):
        return 2
