import logging

from svgfig_base import SvgFigGenerator
from attributes.common import Boolean, Color

from lib.svgfig import *


class Slices(SvgFigGenerator):

    def __init__(self):
        SvgFigGenerator.__init__(self)
        self.has_borders = True
        self.has_space = False
        self.has_single_color = False
        self.color = "0000ff"

    def get_defs(self):
        defs = SVG("defs", id="defs")
        return defs

    def get_elements(self):
        return SVG("g", self._get_slices())

    # TODO: fix all generators to use some common width
    #       defition instead of hardcoded calculation values
    def _count_sizes(self):
        s = 0.0
        width = 300
        if self.has_borders:
            width -= 7
        if self.has_borders:
            width -= 5 * 3
        for row in self.rows:
            s += row[1]
        sizes = []
        if s == 0: s = 1.0
        # TODO: row order!!!
        for row in self.rows:
            sizes.append(row[1] / s * width)
        return sizes

    def _get_slices(self):
        slices = SVG("g")
        if self.has_single_color:
            colors = [ self.color, self.color, self.color,
                       self.color, self.color, self.color]
        else:
            colors = ["ff0000", "00ffff", "ff00ff",
                      "0000ff", "00ff00", "ffff00"]
        if len(self.rows) != 6:
            logging.error("# wrong number of rows")
        c = 0
        if self.has_borders:
            base_style = "stroke:#000000;stroke-width:1;"
            x = 1
        else:
            base_style = ""
            x = 0                    
        for size in self._count_sizes():
            slices.append(SVG("rect",
                              x = x, width = size,
                              y = 0, height = 200,
                              style=("fill:#" + colors[c] + ";" + base_style)))
            c += 1
            x += size
            if self.has_borders:
                x += 1
            if self.has_space:
                x += 3
        return slices

    def get_description(self):
        return "Rectangle slices at with relative sizes"

    def get_ui_name(self):
        return "Slicezz"

    def get_attributes(self):
        has_borders = Boolean(self, "has_borders", "Borders")
        has_space = Boolean(self, "has_space", "Space between slices")
        has_single_color = Boolean(self, "has_single_color", "Single color")
        color = Color(self, "color", "Slice color")
        return [has_borders, has_space, has_single_color, color]

    def get_rating(self):
        return 3
