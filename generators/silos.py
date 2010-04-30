import logging

from lib.svgfig import *
from svgfig_base import SvgFigGenerator
from attributes.common import Color, Boolean, Title, Integer
from attributes.images import Imagechoice
from lib.number_scaler import NumberScaler


class Bar(object):

    def __init__(self, x, y, width, height, style):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.style = style
        self.shadow_diff = 4
        self.shadow_color = "cccccc"

    def _add_shadow(self, g):
        if hasattr(self, "shadow"):
            g.append(self.shadow.SVG())

    def SVG(self):
        g = SVG("g")
        self._add_shadow(g)
        g.append(SVG("rect",
                     x = self.x,
                     y = self.y - self.height,
                     width = self.width,
                     height = self.height,
                     style = self.style))
        return g

    def add_small_shadow(self):
        if hasattr(self, "shadow"):
            return
        y_shadow = max(self.height - self.shadow_diff, 0)
        shadow_style = "fill:#%s;" % self.shadow_color
        self.x = self.x - 2
        self.shadow = self.__class__(self.x + self.shadow_diff,
                                     self.y,
                                     self.width,
                                     y_shadow,
                                     shadow_style)

    def add_big_shadow(self):
        if hasattr(self, "shadow"):
            return
        shadow_style = "fill:#%s;" % self.shadow_color
        self.x = self.x - 2
        self.shadow = self.__class__(self.x + self.shadow_diff,
                                     self.y,
                                     self.width,
                                     self.height + self.shadow_diff,
                                     shadow_style)


class RoundedBar(Bar):

    def SVG(self):
        g = SVG("g")
        self._add_shadow(g)
        g.append(RoundedRect(x1 = self.x,
                             y1 = self.y - self.height,
                             x2 = self.x + self.width,
                             y2 = self.y + 15 - self.height,
                             r = 10,
                             style = self.style).SVG())
        g.append(SVG("rect",
                     x = self.x,
                     y = self.y + 10 - self.height,
                     width = self.width,
                     height = self.height - 10,
                     style = self.style))
        if self.height < 15:
            g.append(SVG("rect",
                         x = self.x,
                         y = self.y,
                         width = self.width,
                         height = 15,
                         style = "fill:#ffffff;"))
        return g


class TriangleBar(Bar):

    def SVG(self):
        g = SVG("g")
        self._add_shadow(g)
        if self.height > 10:
            g.append(SVG("rect",
                         x = self.x,
                         y = self.y + 10 - self.height,
                         width = self.width,
                         height = self.height - 10,
                         style = self.style))
        ty0 = min(self.y + 11 - self.height, self.y)
        g.append(SVG("path",
                     d=("M %d,%d " % (self.x, ty0) +
                        "L %d,%d " % (self.x + self.width / 2,
                                      self.y - self.height) +
                        "L %d,%d z" % (self.x + self.width, ty0)),
                     style = self.style))
        return g


class Silos(SvgFigGenerator):

    def __init__(self):
        SvgFigGenerator.__init__(self)
        self.font_size = 13
        self.border_color = "000000"
        self.bar_width = 80
        self.grid_count = 5
        self.top_line = 5
        self.bar_head = 1
        self.bar_shadow = 1
        self.bar_color = "800000"
        self.has_meter = True
        self.has_grid = False

    def get_elements(self):
        # edges should be 30 ... [bars] ... 10
        # TODO: we need to modify calc to support different size edges
        if self.has_meter:
            self.calc(edge_width = 20,
                      bar_size = 90,
                      font_size = self.font_size)
        else:
            self.calc(edge_width = 10,
                      bar_size = 90,
                      font_size = self.font_size)
        g = SVG("g")
        g.append(self.get_bg())
        g.append(self.get_bar_silos())
        if self.has_grid:
            g.append(gs.Grid(min_level = 160,
                             max_level = 20 + self.top_line,
                             line_height = 1,
                             line_count = self.grid_count + 1,
                             color = self.border_color,
                             has_bline = False).SVG())
        g.append(self.get_bars())
        g.append(self.get_bline())
        g.append(self.get_top_bar())
        if self.has_meter:
            g.append(self.get_meters())
        g.append(self.get_titles())
        return g

    def get_meters(self):
        g = SVG("g")
        style = "fill:#%s;text-anchor:end;font-weight:bold;" % "ffffff"
        bstyle = ("fill:#%s;" % self.border_color +
                  "text-anchor:end;font-weight:bold;")
        k = (160 - (20 + self.top_line)) / (self.grid_count )
        steps = self.get_steps(self.grid_count)
        g.append(Text(30, 165, str(steps[0]), font_size=13, style=bstyle).SVG())
        for i in range(1, self.grid_count + 1):
            y = 160 - i * k
            if y <= 25: continue
            t = NumberScaler().scale(str(steps[i]))
            g.append(Text(30, y + 4, t, font_size=13, style=style).SVG())
        return g        

    def get_steps(self, count):
        step = int((self.max - self.min) / count)
        return range(int(self.min),
                     int(self.max + step),
                     step)
            
    def get_bline(self):
        if self.has_meter:
            return SVG("rect",
                       x = 30, width = 260,
                       y = 160, height = 3,
                       style="fill:#%s;" % self.border_color)
        else:
            return SVG("rect",
                       x = 10, width = 280,
                       y = 160, height = 3,
                       style="fill:#%s;" % self.border_color)

    def get_bg(self):
        g = SVG("g")
        g.append(RoundedRect(0, 20, 300, 200, 20,
                             style="fill:#%s" % self.border_color).SVG())
        g.append(SVG("rect", x=0, y=150, width=300, height=20,
                     style="fill:#ffffff;"))
        return g

    def get_bars(self):
        g = SVG("g")
        bw = self.calc.bar_width * self.bar_width / 100
        bw_x0 = (self.calc.bar_width - bw) / 2
        if self.has_meter:
            bw_x0 += 10
        style = "fill:#%s;" % self.bar_color
        for i in range(0, self.get_row_count()):
            x = self.calc.left(i) + bw_x0
            h = self.get_row_value(i) * (135 - self.top_line)
            if self.bar_head == 1:
                bar = Bar(x, 160, bw, h, style)
            elif self.bar_head == 2:
                bar = RoundedBar(x, 160, bw, h, style)
            elif self.bar_head == 3:
                bar = TriangleBar(x, 160, bw, h, style)
            else:
                logging.info("ERROR: bar_head == %d" % self.bar_head)
                return SVG("g")
            if self.bar_shadow == 2:
                bar.add_small_shadow()
            elif self.bar_shadow == 3:
                bar.add_big_shadow()
            g.append(bar.SVG())
        return g

    def get_bar_silos(self):
        g = SVG("g")
        for i in range(0, self.get_row_count()):
            x = self.calc.left(i)
            if self.has_meter:
                x += 10
            h = self.get_row_value(i) * 140 - self.top_line
            g.append(SVG("rect",
                         x = x,
                         y = 0,
                         width = self.calc.bar_width,
                         height = 190,
                         style = "fill:#ffffff;"))
        return g

    def get_top_bar(self):
        return SVG("rect", x=10, y=20, width=280, height=self.top_line,
                   style="fill:#%s;" % self.border_color)

    def get_titles(self):
        g = SVG("g")
        style = ("fill:#%s;" % self.border_color +
                 "text-anchor:middle;font-weight:bold;")
        fs = self.calc.font_size
        for i in range(0, self.get_row_count()):
            x = self.calc.middle(i)
            name = self.get_row_name(i, max_len=6)
            if self.has_meter:
                x += 10
            g.append(Text(x, 180, name, font_size=fs, style=style).SVG())
        return g

    def get_description(self):
        return "Bars are within silos"

    def get_ui_name(self):
        return "Silos"

    def get_attributes(self):
        has_grid = Boolean(self, "has_grid", "Grid?")
        grid_count = Integer(self, "grid_count", "Grid Count:", 3, 8, 5)
        has_meter = Boolean(self, "has_meter", "Meter?")
        border_color = Color(self, "border_color", "Border Color")
        bar_title = Title(self, "Bar")
        bar_head = Imagechoice(self, "bar_head", "Head",
                               ["silos1", "silos2", "silos3"])
        bar_shadow = Imagechoice(self, "bar_shadow", "Shadow",
                               ["silos1", "silos4", "silos5"])
        bar_color = Color(self, "bar_color", "Color")
        return [has_grid, grid_count, has_meter, border_color,
                bar_title, bar_head, bar_shadow, bar_color]

    def get_version(self):
        return 2
