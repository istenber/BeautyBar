import logging

from svgfig_base import SvgFigGenerator
from attributes.common import Color, Boolean, Choice

from lib.svgfig import *


class Gradient(SvgFigGenerator):

    def __init__(self):
        SvgFigGenerator.__init__(self)
        self.color = "ffff00"
        self.bgcolor = "ffffee"
        self.fc = "000000"
        self.has_titles = True
        self.has_grid = True
        self.grid_style = 1

    def get_defs(self):
        defs = SVG("defs", id="defs")
        gradient = SVG("linearGradient", id="gradient0",
                       x1="0", y1="1", x2="0", y2="0")
        stop = SVG("stop", offset=0.0, style="stop-color:#" + self.fc + ";")
        gradient.append(stop)
        stop = SVG("stop", offset=0.5, style="stop-color:#" + self.color + ";")
        gradient.append(stop)
        stop = SVG("stop", offset=0.9, style="stop-color:#ffffff;")
        gradient.append(stop)
        defs.append(gradient)
        return defs

    def get_elements(self):
        e = SVG("g", 
                self.get_frame(),
                self.get_bars())
        if self.has_titles:
            e.append(self.get_titles())
        return e

    def get_grid_style(self):
        s = "stroke:#" + self.fc + ";stroke-width:1;"
        if self.grid_style == 2:
            s += "stroke-dasharray:1,2;stroke-dashoffset:0"
        elif self.grid_style == 3:
            s += "stroke-dasharray:1,5;stroke-dashoffset:0"
        return s        

    # TODO: make more common methods like get grid?
    def get_grid(self):
        grid = SVG("g")
        style = self.get_grid_style()
        bline = 160 if self.has_titles else 180
        for i in range(1, 5):
            y = bline + 10 - 30 * i
            grid.append(SVG("path", style=style,
                            d="M 20, " + str(y) + " L 280, " + str(y)))
        return grid

    def get_frame(self):
        frame = SVG("g")
        frame.append(SVG("rect", x=5, y=5, width=290, height=190,
                         style="fill:#" + self.color + ";stroke-width:5;" +
                         "stroke-linejoin:round;stroke:#" + self.fc + ";")) 
        bline = 160 if self.has_titles else 180
        frame.append(SVG("rect", x=20, y=20, width=260,
                         height=bline - 20,
                         style="fill:#" + self.bgcolor + ";stroke-width:5;" +
                         "stroke-linejoin:round;stroke:#" + self.fc + ";"))
        s = "stroke-width:3;stroke-linecap:round;stroke:#" + self.fc + ";"
        if self.has_titles:
            l = "M X," + str(bline) + " L X," + str(bline+10)
            for i in range(0, 7):
                x = 30 + i * 40
                frame.append(SVG("path", style=s, d=l.replace("X", str(x))))
        if self.has_grid:
            frame.append(self.get_grid())
        return frame

    def get_titles(self):
        titles = SVG("g")
        text_style = "fill:#" + self.fc + "; text-anchor:middle;"
        for i in range(0, 6):
            x = 50 + i * 40
            name = self.get_row_name(i, max_len=7)
            t = Text(x, 180, name, font_size=10, style=text_style).SVG()
            titles.append(t)
        return titles

    def get_bars(self):
        bars = SVG("g")
        style = ("stroke-width:3;stroke-linejoin:round;" +
                 "stroke:#" + self.fc + ";fill:url(#gradient0);")
        for i in range(0, 6):
            h = self.get_row_value(i) * 120
            # 240 / 6 = 40, 30 + (8 + 24 + 8)*6 + 30
            x = 38 + i * 40
            bar = SVG("rect", x=x, width=24, height=h, style=style,
                      y=(160-h) if self.has_titles else (180-h))
            bars.append(bar)
        return bars

    def get_description(self):
        return "Bars are filled with linear gradient"

    def get_ui_name(self):
        return "Gradient Bars"

    def get_attributes(self):
        color = Color(self, "color", "Color")
        bgcolor = Color(self, "bgcolor", "Background Color")
        fc = Color(self, "fc", "Frame Color")
        has_titles = Boolean(self, "has_titles", "Titles")
        has_grid = Boolean(self, "has_grid", "Grid")
        grid_style = Choice(self, "grid_style", "How sparse grid is",
                            ["Solid", "Some", "Lot"])
        return [color, bgcolor, fc, has_titles, has_grid, grid_style]

    def get_rating(self):
        return 4
