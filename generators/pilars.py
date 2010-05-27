import logging

from lib.svgfig import *
from lib.utils import *
from svgfig_base import SvgFigGenerator
from attributes.common import Color, Choice, Boolean


# PATH="/home/sankari/dev/beautybar/generators/"
PATH="/images/"


class Pilars(SvgFigGenerator):

    def __init__(self):
        SvgFigGenerator.__init__(self)
        self.bg_style = 1
        self.pilar_style = 1
        self.text_color = "ffffff"
        self.border_color = "000000"
        self.grid_color = "000000"
        self.has_grid = False
        self.extra_border = False

    def get_elements(self):
        self.calc(edge_width = 10,
                  bar_size = 80,
                  font_size = 13)
        return SVG("g",
                   self.get_bg(),
                   self.get_bars(),
                   self.get_titles())

    def get_bg(self):
        g = SVG("g")
        g.append(SVG("image", x=0, y=0, width=300, height=200,
                     xlink__href=PATH+"pilars-sky%s.png" % self.bg_style))
        g.append(SVG("rect", x=0, y=0, width=300, height=26,
                     style="fill:#ffffff;"))
        g.append(SVG("rect", x=0, y=26, width=300, height=20,
                     style="fill:#%s;" % self.border_color))
        if self.extra_border:
            c = lighter_color(self.border_color, 40)
            g.append(SVG("rect", x=10, y=16, width=280, height=20,
                         style="fill:#%s;" % c))
        if self.has_grid:
            g.append(self.get_grid())
        return g

    # TODO: move to common base?
    def get_grid(self):
        g = SVG("g")
        g.append(SVG("rect", x=0, y=44, width=300, height=2,
                     style="fill:#%s;" % self.grid_color))
        g.append(SVG("rect", x=0, y=152, width=300, height=2,
                     style="fill:#%s;" % self.grid_color))
        n = 6
        k = 1.0 * (153 - 43) / n
        if self.has_grid:
            for i in range(1, n):
                y = 153 - i * k
                g.append(SVG("rect", x=10, y=y, width=280, height=2,
                             style="fill:#%s;" % self.grid_color))
        return g

    def get_bars(self):
        g = SVG("g")
        if self.pilar_style == 1:
            # 68 x 358
            w = self.calc.bar_width
            ph = int(34.0 / w * 179)
            y0 = 124
            x0 = 0
        if self.pilar_style == 2:
            # 83 x 337
            # 84 x 400
            w = self.calc.bar_width + 6
            ph = int(41.0 / w * 168)
            y0 = 123
            x0 = 3
        img = PATH+"pilars-type%s.png" % self.pilar_style
        for i in range(0, self.get_row_count()):
            x = self.calc.left(i)
            h = self.get_row_value(i) * 110
            g.append(SVG("image", x=x-x0, y=y0-h, width=w,
                         height=179, xlink__href=img))
        return g

    def get_titles(self):
        g = SVG("g")
        g.append(SVG("rect", x=0, y=174, width=300, height=26,
                     style="fill:#ffffff;"))
        g.append(SVG("rect", x=0, y=154, width=300, height=20,
                     style="fill:#%s;" % self.border_color))
        if self.extra_border:
            c = lighter_color(self.border_color, 40)
            g.append(SVG("rect", x=10, y=164, width=280, height=20,
                         style="fill:#%s;" % c))
            text_y = 179
        else:
            text_y = 169
        style = "fill:#%s;text-anchor:middle;" % self.text_color
        fs = self.calc.font_size
        for i in range(0, self.get_row_count()):
            x = self.calc.middle(i)
            name = self.get_row_name(i, max_len=6)
            g.append(Text(x, text_y, name, font_size=fs, style=style).SVG())
        return g

    def get_description(self):
        return "Pilars faced with nature background"

    def get_ui_name(self):
        return "Pilars"

    def get_attributes(self):
        pilar_style = Choice(self, "pilar_style", "Pilar style",
                            ["Corinthian", "Ionic"])
        bg_style = Choice(self, "bg_style", "Background style",
                          ["Cloudy sky", "Sky", "Winter", "Mountains", "Hills"])
        text_color = Color(self, "text_color", "Text color")
        border_color = Color(self, "border_color", "Border color")
        extra_border = Boolean(self, "extra_border", "Extra border")
        has_grid = Boolean(self, "has_grid", "Grid?")
        grid_color = Color(self, "grid_color", "Grid color")
        return [pilar_style, bg_style, text_color, border_color, extra_border,
                has_grid, grid_color]

    def get_version(self):
        return 2
