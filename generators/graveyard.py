import logging

from lib.svgfig import *
from svgfig_base import SvgFigGenerator
from attributes.common import Color, Boolean, Choice


class Graveyard(SvgFigGenerator):

    def __init__(self):
        SvgFigGenerator.__init__(self)
        self.cross_color = "000000"
        self.hollow_color = "ffffff"
        self.cross_style = 1
        self.has_plates = True
        self.text_italic = True
        # TODO: 
        self.sky_dark = ""
        self.sky_light = ""
        self.text_color = ""

    def get_defs(self):
        # cross size 50x90
        # TODO: parametrize!!
        bwh = 7
        n = 2
        s = "fill:#%s;" % self.cross_color
        rad = 5
        skewy = 2
        skewx = 3
        cw = 4
        holstyle = "fill:#%s;" % self.hollow_color
        celtrad = 20
        cr2 = 4
        defs = SVG("defs")
        if self.cross_style == 1:
            defs.append(self._normal_cross(s, bwh))
        if self.cross_style == 2:
            defs.append(self._smaller_cross(s, bwh, n))
        if self.cross_style == 3:
            defs.append(self._cross_with_three_circles(s, bwh, rad))
        if self.cross_style == 4:
            defs.append(self._cross_with_end_circle(s, bwh, rad))
        if self.cross_style == 5:
            defs.append(self._skew_cross(s, bwh, skewx, skewy))
        if self.cross_style == 6:
            defs.append(self._hollow_cross(s, bwh, cw, holstyle))
        return defs

    def _normal_cross(self, s, bwh):
        # normal cross
        return SVG("path", d=(" M %s,%s" % (0, 25-bwh) +
                              " L %s,%s" % (25-bwh, 25-bwh) +
                              " L %s,%s" % (25-bwh, 0) +
                              " L %s,%s" % (25+bwh, 0) +
                              " L %s,%s" % (25+bwh, 25-bwh) +
                              " L %s,%s" % (50, 25-bwh) +
                              " L %s,%s" % (50, 25+bwh) +
                              " L %s,%s" % (25+bwh, 25+bwh) +
                              " L %s,%s" % (25+bwh, 90) +
                              " L %s,%s" % (25-bwh, 90) +
                              " L %s,%s" % (25-bwh, 25+bwh) +
                              " L %s,%s" % (0, 25+bwh) +
                              " z"),
                   style=s, id="cross")

    def _smaller_cross(self, s, bwh, n):
        # cross that goes smaller in middle
        return SVG("path", d=(" M %s,%s" % (0, 25-bwh) +
                              " L %s,%s" % (25-bwh+n, 25-bwh+n) +
                              " L %s,%s" % (25-bwh, 0) +
                              " L %s,%s" % (25+bwh, 0) +
                              " L %s,%s" % (25+bwh-n, 25-bwh+n) +
                              " L %s,%s" % (50, 25-bwh) +
                              " L %s,%s" % (50, 25+bwh) +
                              " L %s,%s" % (25+bwh-n, 25+bwh-n) +
                              " L %s,%s" % (25+bwh, 90) +
                              " L %s,%s" % (25-bwh, 90) +
                              " L %s,%s" % (25-bwh+n, 25+bwh-n) +
                              " L %s,%s" % (0, 25+bwh) +
                              " z"),
                   style=s, id="cross")
        
    def _cross_with_three_circles(self, s, bwh, rad):
        # cross with three end circles
        cross = SVG("g", id="cross")
        cross.append(SVG("path", d=(" M %s,%s" % (2, 25-bwh) +
                                    " L %s,%s" % (25-bwh, 25-bwh) +
                                    " L %s,%s" % (25-bwh, 2) +
                                    " L %s,%s" % (25+bwh, 2) +
                                    " L %s,%s" % (25+bwh, 25-bwh) +
                                    " L %s,%s" % (48, 25-bwh) +
                                    " L %s,%s" % (48, 25+bwh) +
                                    " L %s,%s" % (25+bwh, 25+bwh) +
                                    " L %s,%s" % (25+bwh, 88) +
                                    " L %s,%s" % (25-bwh, 88) +
                                    " L %s,%s" % (25-bwh, 25+bwh) +
                                    " L %s,%s" % (2, 25+bwh) +
                                    " z"),
                         style=s))
        cross.append(SVG("circle", cx=2, cy=25, r=rad, style=s))
        cross.append(SVG("circle", cx=2+rad, cy=25-rad, r=rad, style=s))
        cross.append(SVG("circle", cx=2+rad, cy=25+rad, r=rad, style=s))
        
        cross.append(SVG("circle", cx=48, cy=25, r=rad, style=s))
        cross.append(SVG("circle", cx=48-rad, cy=25-rad, r=rad, style=s))
        cross.append(SVG("circle", cx=48-rad, cy=25+rad, r=rad, style=s))

        cross.append(SVG("circle", cx=25, cy=2, r=rad, style=s))
        cross.append(SVG("circle", cx=25-rad, cy=2+rad, r=rad, style=s))
        cross.append(SVG("circle", cx=25+rad, cy=2+rad, r=rad, style=s))

        cross.append(SVG("circle", cx=25, cy=88, r=rad, style=s))
        cross.append(SVG("circle", cx=25-rad, cy=88-rad, r=rad, style=s))
        cross.append(SVG("circle", cx=25+rad, cy=88-rad, r=rad, style=s))
        return cross

    def _cross_with_end_circle(self, s, bwh, rad):
        # cross with end circles
        cross = SVG("g", id="cross")
        cross.append(SVG("path", d=(" M %s,%s" % (2, 25-bwh) +
                                    " L %s,%s" % (25-bwh, 25-bwh) +
                                    " L %s,%s" % (25-bwh, 2) +
                                    " L %s,%s" % (25+bwh, 2) +
                                    " L %s,%s" % (25+bwh, 25-bwh) +
                                    " L %s,%s" % (48, 25-bwh) +
                                    " L %s,%s" % (48, 25+bwh) +
                                    " L %s,%s" % (25+bwh, 25+bwh) +
                                    " L %s,%s" % (25+bwh, 88) +
                                    " L %s,%s" % (25-bwh, 88) +
                                    " L %s,%s" % (25-bwh, 25+bwh) +
                                    " L %s,%s" % (2, 25+bwh) +
                                    " z"),
                         style=s))
        cross.append(SVG("circle", cx=2, cy=25, r=rad, style=s))
        cross.append(SVG("circle", cx=48, cy=25, r=rad, style=s))
        cross.append(SVG("circle", cx=25, cy=2, r=rad, style=s))
        cross.append(SVG("circle", cx=25, cy=88, r=rad, style=s))
        return cross

    def _skew_cross(self, s, bwh, skewx, skewy):
        # cross skewed sides
        return SVG("path", d=(" M %s,%s" % (0 + skewy, 25-bwh) +
                              " L %s,%s" % (25-bwh, 25-bwh) +
                              " L %s,%s" % (25-bwh, skewx) +
                              " L %s,%s" % (25+bwh, 0) +
                              " L %s,%s" % (25+bwh, 25-bwh) +
                              " L %s,%s" % (50, 25-bwh) +
                              " L %s,%s" % (50 - skewy, 25+bwh) +
                              " L %s,%s" % (25+bwh, 25+bwh) +
                              " L %s,%s" % (25+bwh, 90 - skewx) +
                              " L %s,%s" % (25-bwh, 90) +
                              " L %s,%s" % (25-bwh, 25+bwh) +
                              " L %s,%s" % (0, 25+bwh) +
                              " z"),
                   style=s, id="cross")

    def _hollow_cross(self, s, bwh, cw, holstyle):
        # hollow cross
        cross = SVG("g", id="cross")
        cross.append(SVG("path", d=(" M %s,%s" % (0, 25-bwh) +
                                    " L %s,%s" % (25-bwh, 25-bwh) +
                                    " L %s,%s" % (25-bwh, 0) +
                                    " L %s,%s" % (25+bwh, 0) +
                                    " L %s,%s" % (25+bwh, 25-bwh) +
                                    " L %s,%s" % (50, 25-bwh) +
                                    " L %s,%s" % (50, 25+bwh) +
                                    " L %s,%s" % (25+bwh, 25+bwh) +
                                    " L %s,%s" % (25+bwh, 90) +
                                    " L %s,%s" % (25-bwh, 90) +
                                    " L %s,%s" % (25-bwh, 25+bwh) +
                                    " L %s,%s" % (0, 25+bwh) +
                                    " z"),
                         style=s))
        cross.append(SVG("path", d=(" M %s,%s" % (cw, 25-bwh+cw) +
                                    " L %s,%s" % (25-bwh+cw, 25-bwh+cw) +
                                    " L %s,%s" % (25-bwh+cw, cw) +
                                    " L %s,%s" % (25+bwh-cw, cw) +
                                    " L %s,%s" % (25+bwh-cw, 25-bwh+cw) +
                                    " L %s,%s" % (50-cw, 25-bwh+cw) +
                                    " L %s,%s" % (50-cw, 25+bwh-cw) +
                                    " L %s,%s" % (25+bwh-cw, 25+bwh-cw) +
                                    " L %s,%s" % (25+bwh-cw, 90-cw) +
                                    " L %s,%s" % (25-bwh+cw, 90-cw) +
                                    " L %s,%s" % (25-bwh+cw, 25+bwh-cw) +
                                    " L %s,%s" % (cw, 25+bwh-cw) +
                                    " z"),
                         style=holstyle))
        return cross

    def _celtic_cross(self, s, bwh, cw, holstyle, celtrad, cr2):
        # celtic cross
        cross = SVG("g", id="cross")
        cross.append(SVG("circle", cx=25, cy=25, r=celtrad, style=s))
        cross.append(SVG("circle", cx=25, cy=25, r=celtrad-cw, style=holstyle))
        cross.append(SVG("path", d=(" M %s,%s" % (0, 25-bwh) +
                                    " L %s,%s" % (25-bwh-cr2, 25-bwh) +
                                    " L %s,%s" % (25-bwh+n, 25-bwh+n) +
                                    " L %s,%s" % (25-bwh, 25-bwh-cr2) +
                                    " L %s,%s" % (25-bwh, 0) +
                                    " L %s,%s" % (25+bwh, 0) +
                                    " L %s,%s" % (25+bwh, 25-bwh-cr2) +
                                    " L %s,%s" % (25+bwh-n, 25-bwh+n) +
                                    " L %s,%s" % (25+bwh+cr2, 25-bwh) +
                                    " L %s,%s" % (50, 25-bwh) +
                                    " L %s,%s" % (50, 25+bwh) +
                                    " L %s,%s" % (25+bwh+cr2, 25+bwh) +
                                    " L %s,%s" % (25+bwh-n, 25+bwh-n) +
                                    " L %s,%s" % (25+bwh, 25+bwh+cr2) +
                                    " L %s,%s" % (25+bwh, 90) +
                                    " L %s,%s" % (25-bwh, 90) +
                                    " L %s,%s" % (25-bwh, 25+bwh+cr2) +
                                    " L %s,%s" % (25-bwh+n, 25+bwh-n) +
                                    " L %s,%s" % (25-bwh-cr2, 25+bwh) +
                                    " L %s,%s" % (0, 25+bwh) +
                                    " z"),                         
                         style=s))
        return cross

    def get_elements(self):
        self.calc(edge_width = 2,
                  bar_size = 90,
                  font_size = 12)
        return SVG("g",
                   self.get_bg(),
                   self.get_bars(),
                   self.get_titles())

    def get_bg(self):
        g = SVG("g")
        g.append(SVG("rect", x=0, y=25, width=300, height=115,
                     style="fill:#aaaaff;"))
        g.append(SVG("rect", x=0, y=140, width=300, height=15,
                     style="fill:#008800;"))
        g.append(SVG("rect", x=0, y=155, width=300, height=20,
                     style="fill:#00ff00;"))
        for i in range(0, self.get_row_count()):
            x = self.calc.left(i)
            g.append(SVG("rect",
                         x = x,
                         y = 25,
                         width = self.calc.bar_width,
                         height = 115,
                         style = "fill:#8888ff;"))
        return g

    def get_bars(self):
        g = SVG("g")
        for i in range(0, self.get_row_count()):
            x = self.calc.left(i)
            one = SVG("g", transform="translate(%s,0)" % x)            
            if self.get_row_value(i) < 0.1:
                pass
            else:
                sf = 0.5 + self.get_row_value(i) * 0.5
                x0 = self.calc.bar_width / 2 - 25 * sf
                y0 = 60 + 31 * (0.9 - sf) * 2.86
                m = "translate(%s,%s) scale(%s,%s)" % (x0, y0, sf, sf)
                one.append(SVG("use", xlink__href="#cross", transform=m))
            g.append(one)
        return g

    def get_titles(self):
        g = SVG("g")
        if self.text_italic:
            style = "fill:#000080;text-anchor:middle;font-style:italic;"
        else:
            style = "fill:#000080;text-anchor:middle;"
        if self.has_plates:
            plates = "fill:#ffffff;stroke:#000000;stroke-width:1px;"
            platets = "fill:#000000;text-anchor:middle;"
        fs = self.calc.font_size
        for i in range(0, self.get_row_count()):
            x = self.calc.middle(i)
            name = self.get_row_name(i, max_len=6)
            g.append(Text(x, 45, name, font_size=fs, style=style).SVG())
            if self.has_plates:
                xl = self.calc.left(i)            
                g.append(SVG("rect", x=xl+4, y=135,
                             width=self.calc.bar_width - 8,
                             height=10, style=plates))
                value = self.get_row_value_str(i)
                g.append(Text(x, 143, value,
                              font_size=fs-1, style=platets).SVG())
        return g

    def get_description(self):
        return "Graveyard with crosses"

    def get_ui_name(self):
        return "Graveyard"

    def get_attributes(self):
        cross_color = Color(self, "cross_color", "Cross color")
        hollow_color = Color(self, "hollow_color", "Cross hollow color")
        has_plates = Boolean(self, "has_plates", "Plates?")
        text_italic = Boolean(self, "text_italic", "Use italic text style?")
        cross_style = Choice(self, "cross_style", "Cross style",
                             ["1", "2", "3", "4", "5", "6"])
        return [cross_color, hollow_color, cross_style, has_plates, text_italic]

    def get_version(self):
        return 2
