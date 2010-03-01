import logging

from svgfig_base import SvgFigGenerator
from attributes.common import Boolean, Color

from lib.svgfig import *


class Balls(SvgFigGenerator):

    def __init__(self):
        SvgFigGenerator.__init__(self)
        self.has_borders = True
        self.has_single_color = False
        self.color = "0000ff"
        self.bg_color = "ffffff"

    def get_defs(self):
        defs = SVG("defs", id="defs")
        return defs

    def get_elements(self):
        return SVG("g",
                   self._get_background(),
                   self._get_balls())

    def _get_background(self):
        lines = SVG("g")
        x = 45
        for pos in range(1, 7):
            cx = x + (35 / 2.0)
            lines.append(SVG("path", d=("M " + str(cx) + ",0 " +
                                        "L " + str(cx) + ",180 "), 
                             style="stroke:#000000;stroke-width:1;"))
            lines.append(Text(cx, 190,
                              self.rows[pos-1][0],
                              text_anchor="middle",
                              font_size=10).SVG())
            x += 35
        bg = SVG("g",
                 SVG("rect", x=0, y=0, width=300, height=200,
                     style="fill:#" + self.bg_color + ";"),
                 lines)
        return bg

    def _get_balls(self):
        balls = SVG("g")
        if self.has_single_color:
            colors = [ self.color, self.color, self.color,
                       self.color, self.color, self.color]
        else:
            colors = ["ff0000", "00ffff", "ff00ff",
                      "0000ff", "00ff00", "ffff00"]
        if self.has_borders:
            base_style = "stroke:#000000;stroke-width:1;"
        else:
            base_style = ""
        # 300 = 45 + 6 * 35 + 45
        x = 45
        c = 0
        scaler = (self.max - self.min)
        for row in self.rows:
            size = math.sqrt(row[1] / scaler) * 30
            balls.append(SVG("circle",
                             cy = 100,
                             cx = x + (35/2.0), r = size,
                             style=("fill:#" + colors[c] + ";" + base_style)))
            x += 35
            c += 1
        return balls

    def get_description(self):
        return "Balls with relative size"

    def get_ui_name(self):
        return "Ball diagram"

    def get_attributes(self):
        has_borders = Boolean(self, "has_borders", "Borders")
        has_single_color = Boolean(self, "has_single_color", "Single color")
        color = Color(self, "color", "Slice color")
        bg_color = Color(self, "bg_color", "Background color")
        return [bg_color, has_borders, has_single_color, color]
