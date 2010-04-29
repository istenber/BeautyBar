import logging

from lib.svgfig import *
from svgfig_base import SvgFigGenerator
from attributes.common import Color, Boolean, Title
from attributes.images import Imagechoice
from lib.number_scaler import NumberScaler


class Silos(SvgFigGenerator):

    def __init__(self):
        SvgFigGenerator.__init__(self)
        self.font_size = 13
        self.bar_width = 80
        self.grid_count = 8
        self.top_line = 5
        self.bar_head = 1
        self.bar_line = 1
        self.bar_color = "800000"
        self.has_meter = True
        self.has_grid = False

    def get_defs(self):
        # TODO: bar styles
        return SVG("defs")

    def get_elements(self):
        # edges should be 30 ... [bars] ... 10
        # TODO: we need to modify calc to support different size edges
        self.calc(edge_width = 20,
                  bar_size = 90,
                  font_size = self.font_size)
        g = SVG("g")
        g.append(self.get_bg())
        g.append(self.get_bar_silos())
        if self.has_grid:
            g.append(gs.Grid(min_level = 160,
                             max_level = 20 + self.top_line,
                             line_height = 1,
                             line_count = self.grid_count,
                             has_bline = False).SVG())
        g.append(self.get_bars())
        g.append(self.get_bline())
        g.append(self.get_top_bar())
        if self.has_meter:
            # TODO: remove black side
            g.append(self.get_meters())
        g.append(self.get_titles())
        return g

    def get_meters(self):
        g = SVG("g")
        style = "fill:#%s;text-anchor:end;font-weight:bold;" % "ffffff"
        bstyle = "fill:#%s;text-anchor:end;font-weight:bold;" % "000000"
        k = (160 - (20 + self.top_line)) / (self.grid_count - 1)
        steps = self.get_steps(self.grid_count)
        g.append(Text(30, 165, str(steps[0]), font_size=13, style=bstyle).SVG())
        if self.top_line >= 5:
            gc = self.grid_count
        else:
            gc = self.grid_count - 1
        for i in range(1, gc):
            y = 160 - i * k
            t = NumberScaler().scale(str(steps[i]))
            g.append(Text(30, y + 4, t, font_size=13, style=style).SVG())
        return g        

    def get_steps(self, count):
        step = int((self.max - self.min) / count)
        return range(int(self.min),
                     int(self.max + step),
                     step)
            
    def get_bline(self):
        return SVG("rect",
                   x = 30, width = 260,
                   y = 160, height = 3,
                   style="fill:#%s;" % "000000")

    def get_bg(self):
        g = SVG("g")
        g.append(RoundedRect(0, 20, 300, 200, 20,
                             style="fill:#000000;").SVG())
        g.append(SVG("rect", x=0, y=150, width=300, height=20,
                     style="fill:#ffffff;"))
        return g

    def get_bars(self):
        g = SVG("g")
        bw = self.calc.bar_width * self.bar_width / 100
        bw_x0 = (self.calc.bar_width - bw) / 2
        for i in range(0, self.get_row_count()):
            x = self.calc.left(i)
            h = self.get_row_value(i) * 140 - self.top_line
            g.append(SVG("rect",
                         x = x + 10 + bw_x0,
                         y = 160-h,
                         width = bw,
                         height = h,
                         style = "fill:#%s;" % self.bar_color))
        return g

    def get_bar_silos(self):
        g = SVG("g")
        for i in range(0, self.get_row_count()):
            x = self.calc.left(i)
            h = self.get_row_value(i) * 140 - self.top_line
            g.append(SVG("rect",
                         x = x + 10,
                         y = 0,
                         width = self.calc.bar_width,
                         height = 190,
                         style = "fill:#ffffff;"))
        return g

    def get_top_bar(self):
        return SVG("rect", x=10, y=20, width=280, height=self.top_line,
                   style="fill:#000000;")

    def get_titles(self):
        g = SVG("g")
        style = "fill:#%s;text-anchor:middle;font-weight:bold;" % "000000"
        fs = self.calc.font_size
        for i in range(0, self.get_row_count()):
            x = self.calc.middle(i)
            name = self.get_row_name(i, max_len=6)
            g.append(Text(x+10, 180, name, font_size=fs, style=style).SVG())
        return g

    def get_description(self):
        return "Bars are within silos"

    def get_ui_name(self):
        return "Silos"

    def get_attributes(self):
        has_grid = Boolean(self, "has_grid", "Grid?")
        has_meter = Boolean(self, "has_meter", "Meter?")
        bar_title = Title(self, "Bar")
        # TODO: implement
        bar_head = Imagechoice(self, "bar_head", "Head",
                               ["silos1", "silos2", "silos3"])
        bar_line = Imagechoice(self, "bar_line", "Lines",
                               ["silos1", "silos4", "silos5"])
        bar_color = Color(self, "bar_color", "Color")
        return [has_grid, has_meter, bar_title, bar_head, bar_line, bar_color]

    def get_version(self):
        return 2
