import logging

from lib.svgfig import *
from svgfig_base import SvgFigGenerator
from attributes.common import Color, Boolean
from dots import CommonAttributesBase


class Bars3d(SvgFigGenerator, CommonAttributesBase):

    def __init__(self):
        SvgFigGenerator.__init__(self)
        CommonAttributesBase.__init__(self)
        self.bottomcolor = "aaaaaa"

    def get_elements(self):
        self.calc(edge_width = 10,
                  bar_size = 60,
                  font_size = 12)
        return SVG("g",
                   self.get_bottom(),
                   self.get_bars())


    def get_bottom(self):
        g = SVG("g")
        g.append(SVG("rect", x=0, y=170, width=300, height=10,
                     style="fill:#%s;" % self.bottomcolor))
        return g

    def get_bars(self):
        g = SVG("g")
        colors = ["ff0000", "00ff00", "0000ff"]
        sb = ("stroke-linecap:round;stroke-linejoin:round;" + 
              "stroke-width:2px;stroke:#%s;" % self.color)
        y0 = 170
        sp = 5
        top_space = 30
        for i in range(0, self.get_row_count()):
            s = sb + "fill:#%s;" % colors[i % len(colors)]            
            x0 = self.calc.left(i)
            x1 = self.calc.middle(i)
            x2 = x0 + self.calc.bar_width
            h = y0 - self.get_row_value(i) * (y0 - top_space)
            g.append(SVG("path",
                         d = (" M %s,%s L %s,%s" % (x0, y0, x0, h) +
                              " L %s,%s L %s,%s z" % (x1, h + sp, x1, y0 + sp)),
                         style = s))
            g.append(SVG("path",
                         d = (" M %s,%s L %s,%s" % (x1, y0 + sp, x1, h + sp) +
                              " L %s,%s L %s,%s z" % (x2, h, x2, y0)),
                         style = s))
            g.append(SVG("path",
                         d = (" M %s,%s L %s,%s" % (x0, h, x1, h - sp) +
                              " L %s,%s L %s,%s z" % (x2, h, x1, h + sp)),
                         style = s))
        return g

    def get_description(self):
        return "3D bars are always nice"

    def get_ui_name(self):
        return "3D bars"

    def get_attributes(self):
        return []

    def get_version(self):
        return 2
