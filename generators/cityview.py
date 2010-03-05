import logging
import random

from svgfig_base import SvgFigGenerator
from attributes.common import Color, Boolean, Title

from lib.svgfig import *
from lib.utils import *

class Cityview(SvgFigGenerator):

    def __init__(self):
        SvgFigGenerator.__init__(self)
        self.color = "000000"
        self.bgcolor = "ffffff"
        self.bgbars_onecolor = False
        self.bgbars_color = "d6ff8f"
        self.fgbars_onecolor = False
        self.fgbars_color = "faffd1"
        random.seed(300)

    def random_color(self):
        if not hasattr(self, "_colors"):
            self._colors = []
            c = ['ff0000', '00ff00', '0000ff',
                 'ff00ff', 'ffff00', '00ffff']
            self._colors += map(lambda c: lighter_color(c, 100), c)
            self._colors += map(lambda c: lighter_color(c, 120), c)
            self._colors += map(lambda c: lighter_color(c, 140), c)
        r = self._colors[int(random.random() * len(self._colors))]
        return "fill:#" + str(r) + ";"

    def get_elements(self):
        self.calc(edge_width = 10,
                  bar_size = 80,
                  font_size = 11)
        return SVG("g",
                   self.get_bg(),
                   self.get_back_bars(),
                   self.get_bars(),
                   self.get_front_bars(),
                   self.get_ground())

    def get_bg(self):
        return SVG("rect", x=0, y=50, width=300, height=100,
                   style="fill:#" + self.bgcolor + ";")

    def get_ground(self):
        g = SVG("g")
        g.append(SVG("rect", x=0, y=149, width=300, height=2,
                     style="fill:#cccccc"))
        g.append(SVG("rect", x=0, y=49, width=300, height=2,
                     style="fill:#888888"))
        g.append(SVG("rect", x=0, y=151, width=300, height=2,
                     style="fill:#888888"))
        g.append(SVG("rect", x=0, y=51, width=300, height=2,
                     style="fill:#cccccc"))
        return g
                 
    def get_front_bars(self):
        def s():
            return "fill:#" + self.fgbars_color + ";"
        bars = SVG("g")
        if self.fgbars_onecolor:
            style_f = s
        else:
            style_f = self.random_color
        for i in range(0, self.get_row_count() - 1):
            m = 100 * min(self.get_row_value(i), self.get_row_value(i+1)) - 20
            if m < 0: continue
            h = int(0.5 * m + 0.5 * random.random() * m)
            x = (self.calc.left(i) + self.calc.left(i+1)) / 2
            bar = SVG("rect", x=x, height=h, style=style_f(),
                      width=int(self.calc.bar_width * 1.2), y=150-h+1)
            bars.append(bar)
        return bars

    def get_back_bars(self):
        def s():
            return "fill:#" + self.bgbars_color + ";"
        bars = SVG("g")
        if self.bgbars_onecolor:
            style_f = s
        else:
            style_f = self.random_color
        for i in range(0, self.get_row_count() - 1):
            h = int(random.random() * 100)
            r0 = int(random.random() * 10)
            x = (self.calc.left(i) + self.calc.left(i+1)) / 2 - r0
            bar = SVG("rect", x=x, height=h, style=style_f(),
                      width=int(self.calc.bar_width * 1.2), y=150-h+1)
            bars.append(bar)
        return bars

    def get_bars(self):
        bars = SVG("g")
        tsw = "fill:#" + self.bgcolor + ";font-weight:bold;text-anchor:middle;"
        tsb = "fill:#" + self.color + ";font-weight:bold;text-anchor:middle;"
        color = "fill:#" + self.color + ";"
        fs = self.calc.font_size
        for i in range(0, self.get_row_count()):
            h = self.get_row_value(i) * 100
            x = self.calc.left(i)
            bar = SVG("rect", x=x, height=h, style=color,
                      width=self.calc.bar_width, y=150-h)
            bars.append(bar)
            name = self.get_row_name(i, max_len=6)
            xm = self.calc.middle(i)
            if h < 20:
                t = Text(xm, 148-h, name, font_size=fs, style=tsb).SVG()
            else:
                t = Text(xm, 162-h, name, font_size=fs, style=tsw).SVG()
            bars.append(t)
        return bars

    def get_description(self):
        return "Looks like a city - or not"

    def get_ui_name(self):
        return "City View"

    def get_attributes(self):
        color = Color(self, "color", "Main color")
        bgcolor = Color(self, "bgcolor", "Inverse color")
        bgtitle = Title(self, "Background bars")
        bgbars_onecolor = Boolean(self, "bgbars_onecolor", "All are same color")
        bgbars_color = Color(self, "bgbars_color", "Color")
        fgtitle = Title(self, "Foreground bars")
        fgbars_onecolor = Boolean(self, "fgbars_onecolor", "All are same color")
        fgbars_color = Color(self, "fgbars_color", "Color")
        return [color, bgcolor,
                bgtitle, bgbars_onecolor, bgbars_color,
                fgtitle, fgbars_onecolor, fgbars_color]

    def get_version(self):
        return 2
