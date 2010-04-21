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
        g.append(SVG("rect", x=0, y=0, width=300, height=20,
                     style="fill:#ffffff;"))
        g.append(SVG("rect", x=0, y=20, width=300, height=20,
                     style="fill:#%s;" % self.border_color))
        if self.extra_border:
            c = lighter_color(self.border_color, 40)
            g.append(SVG("rect", x=10, y=10, width=280, height=20,
                         style="fill:#%s;" % c))
        return g

    def get_bars(self):
        g = SVG("g")
        if self.pilar_style == 1:
            # 68 x 358
            ph = int(34.0 / self.calc.bar_width * 179)
        if self.pilar_style == 2:
            # 83 x 337
            ph = int(41.0 / self.calc.bar_width * 168)
        img = PATH+"pilars-type%s.png" % self.pilar_style
        for i in range(0, self.get_row_count()):
            x = self.calc.left(i)
            h = self.get_row_value(i) * 100
            g.append(SVG("image", x=x, y=125-h, width=self.calc.bar_width,
                         height=179, xlink__href=img))
        return g

    def get_titles(self):
        g = SVG("g")
        g.append(SVG("rect", x=0, y=180, width=300, height=20,
                     style="fill:#ffffff;"))
        g.append(SVG("rect", x=0, y=160, width=300, height=20,
                     style="fill:#%s;" % self.border_color))
        if self.extra_border:
            c = lighter_color(self.border_color, 40)
            g.append(SVG("rect", x=10, y=170, width=280, height=20,
                         style="fill:#%s;" % c))
            text_y = 185
        else:
            text_y = 175
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
        return [pilar_style, bg_style, text_color, border_color, extra_border]

    def get_version(self):
        return 2
