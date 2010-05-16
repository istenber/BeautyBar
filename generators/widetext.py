import logging

from lib.svgfig import *
from svgfig_base import SvgFigGenerator
from attributes.common import Color, Boolean, Integer, Float


class Widetext(SvgFigGenerator):

    def __init__(self):
        SvgFigGenerator.__init__(self)
        self.color_a = "60ffff"
        self.color_b = "ffa020"
        self.has_borders = False
        self.border_color = "000000"
        self.y0 = 0
        self.font_size = 20
        self.x0 = 1.0

    # TODO: add cut paths?
    def get_defs(self):
        return SVG("defs")

    def get_elements(self):
        g = SVG("g")
        g.append(self.get_bg())
        g.append(self.get_bars())
        g.append(self.get_titles())
        if self.has_borders:
            g.append(self.get_borders())
        return g

    def get_bg(self):
        g = SVG("g")
        return g

    def get_borders(self):
        g = SVG("g")
        h = (200 - self.y0 * 2) / self.get_row_count()
        h0 = self.y0 + ((200 - self.y0 * 2) % self.get_row_count()) / 2
        style = "fill:#%s;" % self.border_color
        for i in range(1, self.get_row_count()):
            g.append(SVG("rect",
                         x = 0,
                         y = h0 + h * i - 1,
                         width = 300,
                         height = 2,
                         style = style))
        g.append(SVG("rect",
                     x = 0,
                     y = 0,
                     width = 300,
                     height = h0 + 1,
                     style = style))
        g.append(SVG("rect",        
                     x = 0,
                     y = h0 + self.get_row_count() * h - 1,
                     width = 300,
                     height = 300 - h0 + self.get_row_count() * h - 1,
                     style = style))
        return g

    def get_bars(self):
        g = SVG("g")
        h = (200 - self.y0 * 2) / self.get_row_count()
        h0 = self.y0 + ((200 - self.y0 * 2) % self.get_row_count()) / 2
        style_a = "fill:#%s;" % self.color_a
        style_b = "fill:#%s;" % self.color_b
        for i in range(0, self.get_row_count()):
            w = self.get_row_value(i) * 300
            g.append(SVG("rect",
                         x = 0,
                         y = h0 + h * i,
                         width = w,
                         height = h,
                         style = style_a))
            g.append(SVG("rect",
                         x = w,
                         y = h0 + h * i,
                         width = 300-w,
                         height = h,
                         style = style_b))
        return g

    def get_titles(self):
        g = SVG("g")
        h = (200 - self.y0 * 2) / self.get_row_count()
        h0 = (self.y0 + ((200 - self.y0 * 2) % self.get_row_count()) / 2 +
              h / 2 + self.font_size / 2)
        style_a = "fill:#%s;text-anchor:middle;font-weight:bold;" % self.color_a
        style_b = "fill:#%s;text-anchor:middle;font-weight:bold;" % self.color_b
        x0 = 50 + self.x0 * 200 / 2
        for i in range(0, self.get_row_count()):
            w = self.get_row_value(i) * 300
            name = self.get_row_name(i, max_len=10)
            y = h0 + h * i
            # TODO: cut path to w
            g.append(Text(x0, y, name, 
                          font_size=self.font_size + 1, style=style_a).SVG())
            # TODO: cut path from w
            g.append(Text(x0, y, name, 
                          font_size=self.font_size - 1, style=style_b).SVG())
        return g

    def get_description(self):
        return "Horizontal style with wide text"

    def get_ui_name(self):
        return "Wide Text"

    def get_attributes(self):
        color_a = Color(self, "color_a", "Bar color")
        color_b = Color(self, "color_b", "Empty color")
        has_borders = Boolean(self, "has_borders", "Borders?")
        border_color = Color(self, "border_color", "Border color")
        y0 = Integer(self, "y0", "Top space", 0, 20, 10)
        font_size = Integer(self, "font_size", "Font size", 10, 25, 20)
        x0 = Float(self, "x0", "Title position", 0.0, 2.0)
        return [color_a, color_b, has_borders, border_color, y0, font_size, x0]

    def get_version(self):
        return 2
