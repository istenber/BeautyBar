import logging

from svgfig_base import SvgFigGenerator
from attributes.common import Color, Boolean, Integer, Title

from lib.svgfig import *


class Sunnysky(SvgFigGenerator):

    def __init__(self):
        SvgFigGenerator.__init__(self)
        self.barcolor = "ffff00"
        self.bgcolor = "2222ff"
        self.textcolor = "2222ff"
        self.suncolor = "cccc00"
        self.has_borders = True
        self.sun_x = 240
        self.sun_y = 10
        self.sun_r = 20
        self.sun_rot0 = 0
        self.sun_rots = 360
        self.sun_sl_a = 10
        self.sun_sl_l = 40

    def get_elements(self):        
        return SVG("g",
                   self.get_bg(),
                   self.get_sun(),
                   self.get_bars(),
                   self.get_names(self.textcolor, 25, 50, 180, 10))

    # TODO: move to common funcs..
    def get_names(self, color, b0, bx, y, fs, bold=True):
        g = SVG("g")
        if bold:
            ts = "fill:#%s;text-anchor:middle;font-weight:bold;" % color
        else:
            ts = "fill:#%s;text-anchor:middle;" % color
        for i in range(0, 6):
            x = b0 + bx * i
            name = self.get_row_name(i, max_len=6)
            g.append(Text(x, y, name, font_size=fs, style=ts).SVG())
        return g

    def get_sun(self):
        g = SVG("g")
        cx = self.sun_x
        cy = self.sun_y
        r = self.sun_r
        m = self.sun_sl_a
        l = self.sun_sl_l
        style = "fill:#%s;" % self.suncolor
        dist = cy + r + 10
        d = "M %d,%d L %d,%d L %d,%d z" % (cx-5, dist+l,
                                           cx, dist,
                                           cx+5, dist+l)
        g.append(SVG("circle", cx=cx, cy=cy, r=r, style=style))
        for i in range(0, m):
            rot = self.sun_rots / m * i - self.sun_rot0
            g.append(SVG("path", d=d, style=style,
                         transform="rotate(%d, %d, %d)" % (rot, cx, cy)))
        return g

    def get_bg(self):
        if self.has_borders:
            s = "fill:#%s;stroke:#000000;strokewidth:1px;" % self.bgcolor
        else:
            s = "fill:#%s;" % self.bgcolor
        return SVG("rect", x=20, y=1, width=260, height=159, style=s)

    def get_bars(self):
        g = SVG("g")
        if self.has_borders:
            s = "fill:#%s;stroke:#000000;strokewidth:1px;" % self.barcolor
        else:
            s = "fill:#%s;" % self.barcolor
        for i in range(0, 6):
            h = self.get_row_value(i) * 160
            x = 50 * i
            g.append(SVG("rect", x=x+10, y=170-h, height=h, width=30, style=s))
                         
        return g

    def get_description(self):
        return "Sunny sky gives summer feeling"

    def get_ui_name(self):
        return "Sunny Sky"

    def get_attributes(self):
        barcolor = Color(self, "barcolor", "Bar Color")
        bgcolor = Color(self, "bgcolor", "Background Color")
        textcolor = Color(self, "textcolor", "Text Color")
        has_borders = Boolean(self, "has_borders", "Borders for bars")
        sun_title = Title(self, "Sun")
        sun_color = Color(self, "suncolor", "Color")
        sun_x = Integer(self, "sun_x", "X Coordinate", 0, 300, 240)
        sun_y = Integer(self, "sun_y", "Y Coordinate", 0, 200, 10)
        sun_r = Integer(self, "sun_r", "Size", 0, 50, 20)
        sun_rot0 = Integer(self, "sun_rot0", "Rotate start point", 0, 360, 0)
        sun_rots = Integer(self, "sun_rots", "Rotate angle", 0, 360, 360)
        sun_sl_a = Integer(self, "sun_sl_a", "Slice amount", 0, 50, 20)
        sun_sl_l = Integer(self, "sun_sl_l", "Slice length", 10, 60, 40)
        return [barcolor, bgcolor, textcolor, has_borders,
                sun_title, sun_color, sun_x, sun_y, sun_r,
                sun_rot0, sun_rots, sun_sl_a, sun_sl_l]

    def get_version(self):
        return 1
