import logging

from svgfig_base import SvgFigGenerator
from attributes.common import Color, Boolean, Float

from lib.svgfig import *


def _darker(part, amount):
    c = int(part, 16)
    c -= amount
    if c < 0:
        return "00"
    else:
        return hex(c)[2:4]

def color_to_darker(color, amount):
    return (_darker(color[0:2], amount) +
            _darker(color[2:4], amount) +
            _darker(color[4:6], amount))  
    

class Equalizer(SvgFigGenerator):

    def __init__(self):
        SvgFigGenerator.__init__(self)
        self.color = "808000"
        self.has_background = False
        self.how_sparse = 3

    def get_defs(self):
        defs = SVG("defs", id="defs")
        return defs

    def get_elements(self):
        return SVG("g", 
                   self._get_background(),
                   self._get_bars())

    def _get_background(self):
        if not self.has_background:
            return SVG("g")
        lines = SVG("g")
        for pos in range(0, 5):
            y = 40 + 30*pos
            line = SVG("path", d="M 0," + str(y) + " L 300," + str(y),
                       style="stroke:#" + self.color + ";stroke-width:2;")
            lines.append(line)
        bg = SVG("g",
                 SVG("rect", x=0, y=0, width=300, height=200,
                     style="fill:#" + color_to_darker(self.color, 10) + ";"),
                 lines)
        return bg

    def _get_one(self, color, x, val):
        g = SVG("g")
        sparse = self.how_sparse
        for y in range(0, int(math.floor(val / sparse))):
            g.append(SVG("rect", height = 2, width = 35,
                         x = x + 4, y = 180 - (y * sparse - 1),
                         style="fill:#000000;"))
            g.append(SVG("rect", height = 2, width = 35,
                         x = x, y = 180 - (y * sparse),
                         style="fill:#" + color + ";"))
        return g

    def _get_bars(self):
        bars = SVG("g")
        colors = ["ff0000", "00ffff", "ff00ff", "0000ff", "00ff00", "ffff00"]
        if len(self.rows) != 6:
            logging.error("# wrong number of rows")
        for bar in range(0, 6):
            # 300 - (35+7) * 6 = 60... width=35+4
            x = 26 + 42 * bar
            value = ((self.rows[bar][1] - self.min) *
                     # TODO: baseline + scaling
                     135.0 / (self.max - self.min))
            bars.append(self._get_one(colors[bar], x, value))
        return bars

    def get_description(self):
        return "It looks like equalizer"

    def get_ui_name(self):
        return "Equalizer!"

    def get_attributes(self):
        has_background = Boolean(self, "has_background", "Background")
        color = Color(self, "color", "Background color")
        how_sparse = Float(self, "how_sparse", "How sparse bars", 2.0, 6.0)
        return [has_background, color, how_sparse]

    def get_rating(self):
        return 4
