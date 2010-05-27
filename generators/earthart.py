import logging

from lib.svgfig import *
from svgfig_base import SvgFigGenerator
from attributes.common import Color, Boolean, Choice

# PATH="/home/sankari/dev/beautybar/generators/"
PATH="/images/"

class Earthart(SvgFigGenerator):

    def __init__(self):
        SvgFigGenerator.__init__(self)
        self.color = "800000"
        self.has_grid = True
        # self.has_bar_borders = True
        self.style = 3

    def get_elements(self):
        self.calc(edge_width = 10,
                  bar_size = 80,
                  font_size = 14)
        return SVG("g",
                   self.get_bg(),
                   self.get_grid(),
                   self.get_mask(),
                   self.get_bars(),
                   # self.get_bar_borders(),
                   self.get_titles())

    def get_grid(self):
        g = SVG("g")
        g.append(SVG("path", d="M 0,160 L 300,160",
                     style="stroke:#%s;stroke-width:4px;" % self.color))
        if self.has_grid:
            for i in range(1, 7):
                y = 160 - i * 20
                g.append(SVG("path", d="M 2,%s L 298,%s" % (y, y),
                             style="stroke:#%s;stroke-width:2px;" % self.color))
        return g

    def get_bg(self):
        g = SVG("g")
        g.append(SVG("image", x=0, y=0, width=300, height=200,
                     xlink__href=PATH+"earthart-%s-img.jpg" % self.style))
        g.append(SVG("rect", x=0, y=0, width=300, height=40,
                     style="fill:#888888;"))
        g.append(SVG("rect", x=0, y=160, width=300, height=40,
                     style="fill:#888888;"))
        return g
    
    def get_mask(self):
        g = SVG("g")
        g.append(SVG("image", x=0, y=0, width=300, height=200,
                     xlink__href=PATH+"earthart-%s-mask.png" % self.style))
        g.append(SVG("rect", x=0, y=165, width=300, height=25,
                     style="fill:#000000;"))
        return g

    def get_bars(self):
        g = SVG("g")
        for i in range(0, self.get_row_count()):
            x = self.calc.left(i)
            h = self.get_row_value(i) * 120
            g.append(SVG("rect",
                         x = x,
                         y = 160-h,
                         width = self.calc.bar_width,
                         height = h,
                         style = "fill:#%s;" % self.color))
        return g

#     def get_bar_borders(self):
#         g = SVG("g")
#         s = "fill:none;stroke:#%s;stroke-width:2px" % self.color
#         if self.has_bar_borders:
#             for i in range(0, self.get_row_count()):
#                 x = self.calc.left(i)
#                 h = self.get_row_value(i) * 120
#                 g.append(SVG("rect",
#                              x = x,
#                              y = 160-h,
#                              width = self.calc.bar_width,
#                              height = h,
#                              style = s))
#         return g

    def get_titles(self):
        g = SVG("g")
        style = "fill:#%s;text-anchor:middle;font-weight:bold;" % self.color
        fs = self.calc.font_size
        for i in range(0, self.get_row_count()):
            x = self.calc.middle(i)
            name = self.get_row_name(i, max_len=6)
            g.append(Text(x, 180, name, font_size=fs, style=style).SVG())
        return g

    def get_description(self):
        return "From earth we get nice ornaments"

    def get_ui_name(self):
        return "Earth art"

    def get_attributes(self):
        color = Color(self, "color", "Color?")
        has_grid = Boolean(self, "has_grid", "Grid?")
        # has_bar_borders = Boolean(self, "has_bar_borders", "Bar borders?")
        style = Choice(self, "style", "Style?", ["Grass", "Flower", "Dots"])
        return [color, has_grid, style]

    def get_version(self):
        return 2
