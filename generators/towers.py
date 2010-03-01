import logging

from svgfig_base import SvgFigGenerator
from attributes.common import Color, Boolean, Title, Integer

from lib.svgfig import *
from lib.utils import *

# TODO: corporate name
# TODO: color theme
# TODO: common attribute color theme?
# TODO: move many common functions to svgbase or somewhere else
#       get_bg, get_grid, get_bars, ...

class Towers(SvgFigGenerator):

    def __init__(self):
        SvgFigGenerator.__init__(self)
        self.color = "0000ff"
        self.border_width = 8
        self.space_between = 10
        self.has_frame = True
        self.has_grid = True
        self.bold_font = True
        self.bgcolor = "cccccc"

    def get_elements(self):
        c0 = self.bgcolor
        c1 = darker_color(self.bgcolor, 30)
        c2 = darker_color(self.bgcolor, 60)        
        return SVG("g",
                   self.get_bg(c0),
                   self.get_grid(c1, c2),
                   self.get_frame(c2),
                   self.get_bars(),
                   self.get_names(c2))

    def get_names(self, color):
        g = SVG("g")
        if self.bold_font:
            style="fill:#" + color + ";text-anchor:middle;font-weight:bold;"
            fs = 11
        else:
            style="fill:#" + color + ";text-anchor:middle;"
            fs = 13
        for i in range(0, 6):
            x = 37 + 45 * i
            name = self.get_row_name(i, max_len=6)
            g.append(Text(x, 190, name, font_size=fs, style=style).SVG())
        return g
    
    def get_bg(self, color):
        return SVG("rect", x=0, y=0, width=300, height=200,
                   style="fill:#" + color + ";")

    def get_frame(self, color):
        if self.has_frame:
            style = "stroke:#" + color + ";stroke-width:4px;fill:none"
            return SVG("rect", x=2, y=2, width=296, height=196, style=style)
        return SVG("g")

    def get_grid(self, color1, color2):
        g = SVG("g")
        g.append(SVG("rect", x=0, y=170, width=300, height=4,
                     style="fill:#" + color2 + ";"))
        if self.has_grid:
            for i in range(1, 8):
                y = 170 - i * 20
                g.append(SVG("rect", x=10, y=y, width=280, height=2,
                             style="fill:#" + color1 + ";"))
        return g

    def get_bars(self):
        g = SVG("g")
        bar_style = "fill:#" + darker_color(self.color, 127) + ";"
        border_style = "fill:#" + self.color + ";"
        bw_half = self.border_width / 2
        sp_half = self.space_between / 2
        # 15... [45][45][45][45][45][45] ... 15
        # 45=space/border/bar...
        bar_width = 45 - self.space_between - self.border_width
        for i in range(0, 6):
            x = 15 + 45 * i
            h = self.get_row_value(i) * 160            
            g.append(SVG("rect", x=x+sp_half+bw_half,
                         y=170-h, width=bar_width, height=h,
                         style=bar_style))
            if h > 10:
                g.append(SVG("rect", x=x+sp_half,
                             y=170-h+10, width=self.border_width, height=h-10,
                             style=border_style))
                g.append(SVG("rect", x=x+sp_half+bar_width,
                             y=170-h+10, width=self.border_width, height=h-10,
                             style=border_style))
        return g        

    def get_description(self):
        return "Basic bar chart with nice towers"

    def get_ui_name(self):
        return "Towers"

    def get_attributes(self):
        color = Color(self, "color", "Color")
        bgcolor = Color(self, "bgcolor", "Background colorbase")
        has_frame = Boolean(self, "has_frame", "Frame for chart")
        bold_font = Boolean(self, "bold_font", "Use bold font")
        has_grid = Boolean(self, "has_grid", "Show grid")
        bw = Integer(self, "border_width", "Border bar width", 4, 20, 8)
        sp = Integer(self, "space_between", "Space between bars", 2, 20, 10)
        return [color, bgcolor, has_frame, bold_font, has_grid, bw, sp]

    def get_rating(self):
        return 3

    def get_version(self):
        return 1
