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
        # (300 - (39 + 39)) / 6 = 37
        # maybe 3+30+3 is good
        i = 45
        bar_width=30
        shs = 3
        for row in self.rows:
            name = str(row[0])
            value = (row[1] - self.min) * 135.0 / (self.max - self.min)
            pos = 165-value
            bar = SVG("g",
                      SVG("rect", id="bar_" + name, width=bar_width, x=i,
                          y=pos, height=value,
                          style="fill:#" + self.color + ";"))
            if(self.has_text):
                t = Text(i+bar_width/2.0, 180, name, font_size=11,
                         style="fill:#" + self.color + "; text-anchor:middle;"
                         ).SVG()
                bar.append(t)
            bars.append(bar)
            i += 36
        return bars

    def get_description(self):
        return "Very simple and plain bar diagram"

    def get_ui_name(self):
        return "Plain"

    def get_attributes(self):
        color = Color(self, "color", "Color")
        has_text = Boolean(self, "has_text", "Show titles")
        return [color, has_text]

    def get_rating(self):
        return 4
