import logging

from svgfig_base import SvgFigGenerator
from attributes.common import Color, Boolean

from lib.svgfig import *
from lib.utils import *


class Blocks(SvgFigGenerator):

    def __init__(self):
        SvgFigGenerator.__init__(self)
        self.color = "0000ff"
        self.fill_last = False

    def get_defs(self):
        defs = SVG("defs", id="defs")
        return defs

    def get_elements(self):
        return SVG("g", self._get_bars())

    def _get_one(self, x, val):
        g = SVG("g")
        color = self.color
        step_size = 20
        exact_steps = (val / step_size)
        steps = int(math.floor(exact_steps))
        for y in range(0, steps):
            g.append(SVG("rect", height = step_size, width = 40,
                         x = x, y = 160 - (y * (step_size + 10)),
                         style="fill:#" + color + ";"))
            color = darker_color(color, 20)
        if self.fill_last:
            final_step_percentace = exact_steps - steps
            h = int(math.floor(step_size * final_step_percentace))
            y = 160 - steps * (step_size + 10) + (step_size - h)
            g.append(SVG("rect", height = h, width = 40,
                         x = x, y = y,
                         style="fill:#" + color + ";"))            
        return g

    def _get_bars(self):
        bars = SVG("g")
        if len(self.rows) != 6:
            logging.error("# wrong number of rows")
        for bar in range(0, 6):
            # 300 - (40+10) * 6 = 300... 5+40+10...+10+40+5
            x = 5 + 50 * bar
            value = ((self.rows[bar][1] - self.min) *
                     135.0 / (self.max - self.min))
            bars.append(self._get_one(x, value))
        return bars

    def get_description(self):
        return "Blocks and more blocks"

    def get_ui_name(self):
        return "Blocks..."

    def get_attributes(self):
        # TODO: step_size as a INTEGER param
        # TODO: darker amount as a INTEGER param
        fill_last = Boolean(self, "fill_last", "Last block partial")
        color = Color(self, "color", "Block color")
        return [fill_last, color]

    def get_rating(self):
        return 3
