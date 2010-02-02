import logging
import math
from random import Random as Rnd

from svgfig_base import SvgFigGenerator
from attributes.common import Choice, Float, Color, Boolean

from lib.svgfig import *
from lib.utils import *


class Plates(SvgFigGenerator):

    def __init__(self):
        SvgFigGenerator.__init__(self)
        self.random = Rnd()
        self.psize = 8.0
        self.ptype = 1
        self.color = "000000"
        self.has_meters = False
        self.has_titles = False

    def get_defs(self):
        defs = SVG("defs", id="defs")
        return defs

    def get_elements(self):
        self.random.seed(1)
        self.precalc()
        g = SVG("g")
        if self.ptype == 1:
            g.append(self.random_squares())
        else:
            g.append(self.random_circles())
        if self.has_titles:
            g.append(self.titles())
        if self.has_meters:
            g.append(self.meters())
        return g

    def precalc(self):
        m = []
        for i in range(0, 6):
            # 300 = 20 * 2 * 6
            # 40, 60... 80, 100... 120, 140...
            x0 = 40 + 40 * i
            x1 = x0 + 20
            y0 = 170 - self.rows[i][1] * 3
            y1 = 170
            bar = (x0, y0, x1, y1)
            m.append(bar)
        line = (20, 160, 280, 170)
        m.append(line)
        self.areas = m

    def in_limits(self, x, y):
        for (x0, y0, x1, y1) in self.areas:
            if x > x0 and x < x1 and y > y0 and y < y1:
                return True
        return False


    def random_circles(self):
        circles = SVG("g")
        for i in range(0, 2000):
            cx = self.random.random() * 300
            cy = self.random.random() * 200
            if self.in_limits(cx, cy):
                r = SVG("circle", cx = cx, cy = cy, r = self.psize / 1.4,
                        style = "fill:#" + self.color + ";")
                circles.append(r)
        return circles

    def random_squares(self):
        squares = SVG("g")
        for i in range(0, 2000):
            x = self.random.random() * 300
            y = self.random.random() * 200
            if self.in_limits(x - self.psize/2 , y + self.psize/2):
                r = SVG("rect", x = x, y = y,
                        width = self.psize, height = self.psize,
                        style = "fill:#" + self.color + ";")
                squares.append(r)
        return squares

    def titles(self):
        titles = SVG("g")
        for i in range(0, 6):
            x = 50 + 40 * i
            t = Text(x, 190, self.rows[i][0], font_size=11,
                     style="fill:#" + self.color + "; text-anchor:middle;"
                     ).SVG()
            titles.append(t)
        return titles

    def meters(self):
        meters = SVG("g")
        for i in range(1, 6):
            y = 170 - i * 30
            m = SVG("path", d = ("M 20," + str(y) + " L 280," + str(y)),
                    style="stroke:#" + self.color + ";stroke-width:2;")
            meters.append(m)
        return meters                

    def get_description(self):
        return "Random pieces end up looking something"

    def get_ui_name(self):
        return "Random plates"

    def get_attributes(self):
        has_meters = Boolean(self, "has_meters", "Meters")
        has_titles = Boolean(self, "has_titles", "Titles")
        psize = Float(self, "psize", "Plate size", 5.0, 15.0)
        ptype = Choice(self, "ptype", "Plate type", ["Squares", "Circles"])
        color = Color(self, "color", "Color")
        return [has_meters, has_titles, psize, ptype, color]

    def get_rating(self):
        return 3
