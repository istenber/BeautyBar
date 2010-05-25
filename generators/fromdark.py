import logging

from lib.svgfig import *
from svgfig_base import SvgFigGenerator
from attributes.common import Color, Float, Choice, Boolean, Title
from attributes.complex import Background


class Fromdark(SvgFigGenerator):

    def __init__(self):
        SvgFigGenerator.__init__(self)
        self.bar_color = "ff0000"
        self.text_color = "ff0000"
        self.darkest = 0.8
        self.bar_fill = 0.8
        self.has_splitter = True
        self.titles_clean = True
        self.background = 'rocks'
        self.bg_opacity = 1.0

    def get_elements(self):
        self.calc(edge_width = 16,
                  bar_size = 80,
                  font_size = 14)
        return SVG("g",
                   self.get_bg(),
                   self.get_silos(),
                   self.get_grid(),
                   self.get_bars(),
                   self.get_baseline(),
                   self.get_titles())

    def get_baseline(self):
        g = SVG("g")
        # remove top!
        g.append(SVG("rect", x=0, width=300, y=0, height=20,
                     style="fill:#ffffff;"))
        if self.titles_clean:
            g.append(SVG("rect", x=0, width=300, y=170, height=30,
                         style="fill:#ffffff;"))
        else:
            g.append(SVG("rect", x=0, width=300, y=190, height=10,
                         style="fill:#ffffff;"))
        lbstyle="stroke:#000000;stroke-width:4px;stroke-linecap:round;"
        g.append(SVG("path", d="M 0,170 L 300,170", style=lbstyle))
        st = "fill:#%s;text-anchor:end;font-weight:bold;" % self.text_color
        st0 = "stroke-width:2px;stroke:#000000"
        g.append(Text(25, 170 - 5, str(int(self.min)), font_size=12,
                          style=st + st0).SVG())
        g.append(Text(25, 170 - 5, str(int(self.min)), font_size=12,
                          style=st).SVG())
        return g

    def get_bg(self):
        return SVG("image", id="bg_image",x=33, y=0,
                   width=267, height=200,
                   xlink__href="/dbimages/nature/%s.jpg" % self.background,
                   style="opacity:%s;" % self.bg_opacity)

    def get_steps(self, count):
        step = int((self.max - self.min) / count)
        return range(int(self.min),
                     int(self.max + step),
                     step)

    def get_grid(self):
        g = SVG("g")
        steps = self.get_steps(6)
        sbstyle="stroke:#000000;stroke-width:1px;stroke-dasharray:1,2;"
        st = "fill:#%s;text-anchor:end;font-weight:bold;" % self.text_color
        st0 = "stroke-width:2px;stroke:#000000"
        for i in range(0, 6):
            y = 150 - i * 20
            g.append(SVG("path", d="M 0,%d L 300,%d" % (y, y), style=sbstyle))
            g.append(Text(25, y - 5, str(steps[i+1]), font_size=12,
                          style=st + st0).SVG())
            g.append(Text(25, y - 5, str(steps[i+1]), font_size=12,
                          style=st).SVG())
        return g

    def get_silos(self):
        g = SVG("g")
        w = (self.calc.bar_width * 100 / 80) + 2
        x0 = 15 - (w - self.calc.bar_width) / 2
        op = self.darkest / 2
        op_dec = op / self.get_row_count()
        for i in range(0, self.get_row_count()):
            x = self.calc.left(i) + x0
            g.append(SVG("rect",
                         x = x,
                         y = 0,
                         width = w,
                         height = 200,
                         style = "opacity:%s;fill:#000000;" % op))
            if self.has_splitter:
                splitter_style = "fill:none;stroke-width:1px;stroke:#000000;"
                g.append(SVG("rect",
                             x = x + 1,
                             y = 0,
                             width = w - 1,
                             height = 200,
                             style = splitter_style))
            op -= op_dec
        return g

    def get_bars(self):
        g = SVG("g")
        for i in range(0, self.get_row_count()):
            x = self.calc.left(i) + 15
            h = self.get_row_value(i) * 120
            g.append(SVG("rect",
                         x = x,
                         y = 170-h,
                         width = self.calc.bar_width,
                         height = h,
                         style = "opacity:%s;fill:#%s;" % (self.bar_fill / 2,
                                                           self.bar_color)))
            g.append(SVG("rect",
                         x = x,
                         y = 170-h,
                         width = self.calc.bar_width,
                         height = h,
                         style = "fill:none;stroke-width:1px;stroke:#000000;"))
        return g

    def get_titles(self):
        g = SVG("g")
        st = "fill:#%s;text-anchor:middle;font-weight:bold;" % self.text_color
        st0 = "stroke-width:2px;stroke:#000000"
        fs = self.calc.font_size
        for i in range(0, self.get_row_count()):
            x = self.calc.middle(i) + 15
            name = self.get_row_name(i, max_len=6)
            g.append(Text(x, 185, name, font_size=fs, style=st + st0).SVG())
            g.append(Text(x, 185, name, font_size=fs, style=st).SVG())
        return g

    def get_description(self):
        return "Here are some darker parts in left"

    def get_ui_name(self):
        return "From dark"

    def get_attributes(self):
        bar_title = Title(self, "Bar")
        bar_color = Color(self, "bar_color", "Color")
        bar_fill = Float(self, "bar_fill", "Opacity", 0.2, 1.8)
        bg_title = Title(self, "Background")
        background = Background(self, "background", "Image")
        bg_opacity = Float(self, "bg_opacity", "Opacity", 0.2, 1.8)
        other_title = Title(self, "Other")
        text_color = Color(self, "text_color", "Text color")
        darkest = Float(self, "darkest", "Darkness of left side", 0.2, 1.4)
        has_splitter = Boolean(self, "has_splitter", "Lines between bars?")
        titles_clean = Boolean(self, "titles_clean", "Titles on white?")
        return [bar_title, bar_color, bar_fill,
                bg_title, background, bg_opacity,
                other_title, text_color, darkest, has_splitter, titles_clean]


    def get_version(self):
        return 2
