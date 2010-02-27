import logging
import random

from svgfig_base import SvgFigGenerator
from attributes.common import Color, Boolean, Choice

from lib.svgfig import *

FIGURE_PATH = 'M 39.08866,901.5024 L 43.95708,879.71409 L 54.88733,873.57248 L 58.08736,857.11628 L 50.83599,858.83411 L 50.59276,871.73303 L 38.05869,876.7725 L 35.23111,881.68276 L 29.34032,881.68276 L 26.51274,876.7725 L 13.978673,871.73303 L 13.73544,858.83411 L 6.484073,857.11628 L 9.6841,873.57248 L 20.61436,879.71409 L 25.48284,901.5024 L 19.877132,919.6118 L 9.798188,923.4351 L 8.407202,927.6081 L 27.8658,925.1758 L 30.98982,898.0706 L 33.58176,898.0706 L 36.70578,925.1758 L 56.16438,927.6081 L 54.77338,923.4351 L 44.69444,919.6118 L 39.08866,901.5024 z'

MEDAL_LEFT = 'M 29.970044,886.533 C 29.255839,886.2949 24.494478,876.6531 24.494478,876.6531 L 22.589934,876.058 L 29.851011,887.4852'
MEDAL_RIGHT = 'M 34.373701,886.533 C 35.087906,886.2949 39.849266,876.6531 39.849266,876.6531 L 41.753811,876.058 L 34.492734,887.4852'
MEDAL_GOLD = 'M 30.042724,888.84034 L 30.794181,890.4685 L 31.921369,888.96559 L 31.420394,893.59957 L 33.549521,893.59957 L 32.923308,887.33743 L 30.042724,888.84034 z'
MEDAL_SILVER = 'M 30.164759,888.53499 L 30.72219,889.98431 L 32.728945,888.89732 L 32.728945,890.20728 L 30.610705,892.10255 L 30.053274,892.88295 L 34.512726,892.88295 L 34.401239,891.6566 L 32.283001,891.87958 L 33.955294,889.98431 L 33.843807,887.42013 L 30.164759,888.53499 z'
MEDAL_BRONZE = 'M 30.351633,888.4393 L 30.845019,889.77144 L 32.719893,888.93269 L 33.163942,890.06748 L 32.275844,890.65954 L 32.127828,891.35029 L 33.114603,891.59698 L 33.015925,892.58375 L 31.141054,892.09037 L 30.697006,892.87978 L 32.719893,893.71855 L 34.496087,892.87978 L 33.774461,890.95558 L 34.21851,888.73533 L 32.522538,887.20583 L 30.351633,888.4393 z'
MEDAL_BASE = 'M 36.75,890.61218 A 4.5,4.5 0 1 1 27.75,890.61218 A 4.5,4.5 0 1 1 36.75,890.61218 z'

# TODO: add heads
class Figure(object):

    def __init__(self, x, size, color, text):
        self.x = x
        self.size = size
        self.color = color
        self.text = text

    def add_medal(self, medal):
        if medal in ['gold', 'silver', 'bronze']:
            self.medal = medal

    def get_medal(self, t):
        g = SVG("g")
        rs = "fill:#000000;stroke:#000000;stroke-width:1px;"
        if self.medal == 'gold':
            c = 'ffff00'
            v = MEDAL_GOLD
        elif self.medal == 'silver':
            c = 'cccccc'
            v = MEDAL_SILVER
        else:
            c = 'c87137'
            v = MEDAL_BRONZE
        ms = "fill:#" + c + ";stroke:#000000;stroke-width:1px;"
        g.append(SVG("path", d=MEDAL_LEFT, style=rs, transform=t))
        g.append(SVG("path", d=MEDAL_RIGHT, style=rs, transform=t))
        g.append(SVG("path", d=MEDAL_BASE, style=ms, transform=t))
        g.append(SVG("path", d=v, style=ms, transform=t))
        return g

    def help_line(self):
        return SVG("path",
                   d="M %d,0 L %d,200" % (self.x + 25, self.x + 25),
                   style="stroke-width:1px;stroke:#000000;")

    def output(self):
        # TODO: shadow
        v = self.size
        # x = self.x - 6.2826161
        a = 0.4158 + 0.576 * v
        b = -2.696 - 3.75 * v + self.x + 14.2 - 15 * v
        c = -235.7 - 534 * v
        t = "matrix(%f,0,0,%f,%f,%f)" % (a, a, b, c)
        # + str(a) + 0.9689305,0,0,0.9689305," + str(x) + ",-748.78778)"
        figure = "fill:#" + self.color + ";"
        shadow = "fill:#000000;filter:url(#figure_shadow);"
        g = SVG("g")
        g.append(SVG("path", d=FIGURE_PATH, style=shadow, transform=t))
        g.append(SVG("path", d=FIGURE_PATH, style=figure, transform=t))
        if hasattr(self, "medal"):
            g.append(self.get_medal(t))
        g.append(SVG("rect", x=12, width=40, y=830, height=30,
                     style="fill:#ffffff;stroke:#000000;stroke-width:1px;",
                     transform=t))
        g.append(Text(32, 850, self.text,
                      font_size=17,
                      transform=t,
                      style="fill:#000000;text-anchor:middle;").SVG())   
        # g.append(self.help_line())
        return g

    @classmethod
    def get_defs(cls):
        return SVG("filter", SVG("feGaussianBlur", stdDeviation=2),
                   id="figure_shadow")


class Champions(SvgFigGenerator):

    def __init__(self):
        SvgFigGenerator.__init__(self)
        self.single_color = False
        self.color = "ffa733"
        self.has_medals = True
        self.has_grid = True
        # TODO: more attributes

    def get_defs(self):
        return SVG("defs", Figure.get_defs())

    def get_elements(self):
        return SVG("g",
                   self.get_logo(),
                   self.get_meters(),
                   self.get_names(),
                   self.get_figures())

    def get_logo(self):
        g = SVG("g")
        g.append(SVG("circle", cx=128, cy=20, r=10,
                     style="fill:none;stroke:#000000;stroke-width:2px;"))
        g.append(SVG("circle", cx=150, cy=20, r=10,
                     style="fill:none;stroke:#000000;stroke-width:2px;"))
        g.append(SVG("circle", cx=172, cy=20, r=10,
                     style="fill:none;stroke:#000000;stroke-width:2px;"))
        g.append(SVG("circle", cx=139, cy=31, r=10,
                     style="fill:none;stroke:#000000;stroke-width:2px;"))
        g.append(SVG("circle", cx=161, cy=31, r=10,
                     style="fill:none;stroke:#000000;stroke-width:2px;"))
        return g

    def get_names(self):
        g = SVG("g")
        for i in range(0, 6):
            x = 5 + i * 50
            g.append(SVG("rect", x=x, width=40, y=160, height=20,
                         style="fill:#ffffff;stroke:#000000;stroke-width:1px;"))
            name = self.get_row_name(i, max_len=6)
            g.append(Text(x+20, 175, name, font_size=10,
                          style="fill:#000000;text-anchor:middle;").SVG())
        return g

    def get_meters(self):
        g = SVG("g")
        g.append(SVG("rect", x=0, y=48, width=300, height=2,
                     style="fill:#888888;"))
        g.append(SVG("rect", x=0, y=50, width=300, height=2,
                     style="fill:#aaaaaa;"))
        if self.has_grid:
            for i in range(0, 4):
                g.append(SVG("rect", x=10, y=(118-i*10), width=280, height=2,
                             style="fill:#bbbbbb;"))
        g.append(SVG("rect", x=0, y=150, width=300, height=2,
                     style="fill:#aaaaaa;"))
        g.append(SVG("rect", x=0, y=152, width=300, height=2,
                     style="fill:#888888;"))
        return g

    def get_medalists(self):
        ordered = []
        for i in range(0, 6):
            ordered.append([i, self.get_row_value(i)])
        ordered.sort(cmp=lambda a, b: cmp(a[1], b[1]), reverse=True)
        self.gold = ordered[0][0]
        self.silver = ordered[1][0]
        self.bronze = ordered[2][0]

    def get_figures(self):
        figs = SVG("g")
        colors = ['000080', '008000', '800000',
                  '808000', '008080', '800080']
        self.get_medalists()
        for i in range(0, 6):
            # 300 / 6 = 50
            if self.single_color:
                c = self.color
            else:
                c = colors[i]
            fig = Figure(x = i*50, color = c,
                         size = self.get_row_value(i),
                         text = self.get_row_value_str(i))
            if self.has_medals:
                if self.gold == i:
                    fig.add_medal('gold')
                elif self.silver == i:
                    fig.add_medal('silver')
                elif self.bronze == i:
                    fig.add_medal('bronze')
            figs.append(fig.output())
        return figs

    def get_description(self):
        return "We are the champions"

    def get_ui_name(self):
        return "Champions"

    def get_attributes(self):
        # TODO: add attributes
        single_color = Boolean(self, "single_color",
                               "All figures are same color")
        color = Color(self, "color", "Color of figures")
        has_medals = Boolean(self, "has_medals", "Medals for the champions")
        has_grid = Boolean(self, "has_grid", "Background grid")
        return [single_color, color, has_medals, has_grid]

    def get_rating(self):
        return 3

    def get_version(self):
        return 1
