import logging
import math
from random import Random as Rnd

from svgfig_base import SvgFigGenerator
from attributes.common import Random

from lib.svgfig import *
from lib.utils import *


class Rocks(SvgFigGenerator):

    def __init__(self):
        SvgFigGenerator.__init__(self)
        self.random = Rnd()
        self.seed = 1000

    def get_defs(self):
        defs = SVG("defs", id="defs")
        return defs

    def get_elements(self):
        return SVG("g", self._get_bars())

    def _my_rnd(self):
        return (self.random.random() - 0.5) * 3

    def _get_one(self, x_base, val):
        g = SVG("g")
        colors = ["ff0000", "00ff00", "0000ff",
                  "ffff00", "00ffff", "ff00ff"]
        size = 10.0
        dy = 0.0
        last_dx = 40.0
        while dy < val:
            dx = 0.0
            while dx < last_dx - size:
                cr = int(math.floor(self.random.random() * 6.0 + 0.5)) - 1
                style = ("stroke-width:1px;stroke:#000000;fill:#" +
                         colors[cr] + ";")
                h = size + self._my_rnd()
                w = size + self._my_rnd()
                x0 = x_base + dx + self._my_rnd()
                x1 = x_base + dx - size + self._my_rnd()
                y0 = 160 - dy - size + self._my_rnd()
                y1 = 160 - dy + self._my_rnd()                
                xr = self._my_rnd()
                yr = self._my_rnd()
                d = ("M " + str(x0) + "," + str(y0) +
                     " L " + str(x1 + xr) + "," + str(y0) +
                     " L " + str(x1) + "," + str(y1 + yr) +
                     " L " + str(x0) + "," + str(y1) + " z")
                g.append(SVG("path", d = d, style = style))
                # rectange version
                # g.append(SVG("rect", height = h, width = w,
                #              x = x_base + dx, y = 160 - size - dy,
                #              style = style))
                dx += size
            last_dx = dx
            dy += size
            size -= 0.5
            x_base += 0.5
        return g

    def _get_bars(self):
        self.random.seed(self.seed)
        bars = SVG("g")
        if len(self.rows) != 6:
            logging.error("# wrong number of rows")
        for bar in range(0, 6):
            # TODO: counting...
            x = 20 + 50 * bar
            value = ((self.rows[bar][1] - self.min) *
                     100.0 / (self.max - self.min))
            # some scaling...
            value = value + (value * 0.1 - self.max * 0.1)
            bars.append(self._get_one(x, value))
        return bars

    def get_description(self):
        return "Rock piled top of each others"

    def get_ui_name(self):
        return "Rocks"

    def get_attributes(self):
        seed = Random(self, "seed", "Block randomizer")
        return [seed]

    def get_rating(self):
        return 3
