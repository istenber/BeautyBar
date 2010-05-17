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
        self.font_weight = 3

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
        for i in range(0, self.get_row_count()):
            w = self.get_row_value(i) * 300
            g.append(SVG("rect",
                         x = w - 1,
                         y = h0 + h * i,
                         width = 2,
                         height = h,
                         style = style))
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
        # TODO: make font processing library for svg
        fs = int(self.font_size * (6 / self.get_row_count()))
        h = (200 - self.y0 * 2) / self.get_row_count()
        h0 = (self.y0 + ((200 - self.y0 * 2) % self.get_row_count()) / 2 +
              h / 2 + fs / 2)
        text_style = "text-anchor:middle;font-weight:900;"
        style_a = (text_style + "fill:none;" +
                   "stroke-width:%spx;" % self.font_weight +
                   "stroke:#%s;" % self.color_a)
        style_b = text_style + "fill:#%s;" % self.color_b
        x0 = 50 + self.x0 * 200 / 2
        for i in range(0, self.get_row_count()):
            w = self.get_row_value(i) * 300
            name = self.get_row_name(i, max_len=10)
            y = h0 + h * i
            g.append(Text(x0, y, name, 
                          font_size=fs, style=style_a).SVG())
            g.append(Text(x0, y, name, 
                          font_size=fs, style=style_b).SVG())
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
        y0 = Integer(self, "y0", "Aspect ratio", 0, 20, 10)
        font_size = Integer(self, "font_size", "Font size", 15, 25, 20)
        x0 = Float(self, "x0", "Title position", 0.0, 2.0)
        font_weight = Integer(self, "font_weight", "Font weight",
                              1, 5, 3)
        return [color_a, color_b, has_borders, border_color, y0,
                font_size, x0, font_weight]

    def get_version(self):
        return 2
