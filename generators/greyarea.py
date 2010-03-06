import logging

from svgfig_base import SvgFigGenerator
from attributes.common import Color

from lib.svgfig import *
from lib.utils import *


class Greyarea(SvgFigGenerator):

    def __init__(self):
        SvgFigGenerator.__init__(self)
        self.gcolor = "cccccc"
        self.bcolor = "00ff00"
        self.r0 = 15

    def get_elements(self):
        self.calc(edge_width=20,
                  bar_size=60,
                  font_size=12)
        return SVG("g",
                   self.get_grey_areas(),
                   self.get_meters(),
                   self.get_names(),
                   self.get_bars())

    def get_area(self, width_scaler, h0, style, h):
        g = SVG("g")
        w = int(self.calc.bar_width * width_scaler)
        x0 = int(self.calc.bar_width * (1.0 - width_scaler) * 0.5)
        for i in range(0, self.get_row_count()):
            x = self.calc.left(i) + self.r0 + x0
            g.append(SVG("rect", x=x, y=h0-h, width=w, height=h, style=style))
        return g

    def get_grey_areas(self):
        return self.get_area(1.5, 170, "fill:#%s;" % self.gcolor, 140)

    def get_steps(self, count):
        step = int((self.max - self.min) / count)
        return range(int(self.min),
                     int(self.max + step),
                     step)

    def get_meters(self):
        g = SVG("g")
        steps = self.get_steps(5)
        sbstyle="stroke:#000000;stroke-width:1px;stroke-dasharray:1,2;"
        lbstyle="stroke:#000000;stroke-width:4px;stroke-linecap:round;"
        g.append(SVG("path", d="M 0,150 L 300,150", style=lbstyle))
        g.append(Text(30, 150 - 5, str(steps[0]), font_size=12,
                          style="fill:#000000;text-anchor:end;").SVG())
        for i in range(0, 5):
            y = 130 - i * 20
            g.append(SVG("path", d="M 0,%d L 300,%d" % (y, y), style=sbstyle))
            g.append(Text(30, y - 5, str(steps[i+1]), font_size=12,
                          style="fill:#000000;text-anchor:end;").SVG())
        return g
    
    def get_names(self):
        g = SVG("g")
        for i in range(0, self.get_row_count()):
            x = self.calc.middle(i) + self.r0
            name = self.get_row_name(i)
            g.append(Text(x, 165, name, font_size=self.calc.font_size,
                          style="fill:#000000;text-anchor:middle;").SVG())
        return g

    def get_bars(self):
        g = SVG("g")
        w = self.calc.bar_width
        style = "fill:#%s;stroke:#000000;stroke-width:2px;" % self.bcolor
        for i in range(0, self.get_row_count()):
            x = self.calc.left(i) + self.r0
            h = self.get_row_value(i) * 100 - 1
            g.append(SVG("rect", x=x, y=149-h, width=w, height=h, style=style))
        return g

    def get_description(self):
        return "Bars are rounded with grey area"

    def get_ui_name(self):
        return "Grey Area"

    def get_attributes(self):
        bcolor = Color(self, "bcolor", "Bar color")
        gcolor = Color(self, "gcolor", "Bar back color")
        return [bcolor, gcolor]

    def get_version(self):
        return 2
