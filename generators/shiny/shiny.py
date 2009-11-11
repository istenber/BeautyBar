#!/usr/bin/env python

if __name__ == "__main__":
    import sys
    LIB_PATH = "/home/sankari/dev/beautybar/lib"
    sys.path.append(LIB_PATH + "/svgfig")

import logging
import re

from svgfig import *

def convert_color(style, sub_func):
    str_in = style["style"]
    def _repl(m):
        color = m.group(0)
        # print "color: " + str(color)
        color = sub_func(color)
        # print "color: " + str(color)
        return "#" + color + ";"
    str_out = re.sub(r"#([0-9a-f]*);",
                     _repl,
                     str_in)
    style["style"] = str_out

def red_to_blue(style):
    convert_color(style, lambda c: c[5:7] + c[3:5] + c[1:3])

def red_to_green(style):
    convert_color(style, lambda c: c[3:5] + c[1:3] + c[5:7])

class Bar(object):
    def __init__(self, template):
        self.bar = template.clone()
    def set_color(self, color):
        if color == "red": return
        b = self.bar
        styles = (b[0], b[1, 0], b[1, 1], b[1, 2])
        if color == "blue": f = red_to_blue
        if color == "green": f = red_to_green
        for style in styles:
            f(style)    
    def set_pos(self, pos):
        self.bar["transform"] = "translate(" + pos + ")"

def main():
    """ 
    Convert red.svg to blue.svg and green.svg, and
    combine all together as all.svg.
    """
    logging.getLogger().setLevel(logging.DEBUG)
    svg = load("red.svg")
    attr = svg.attr
    filters = svg[0]
    bar = svg[3, 0]

    rbar = Bar(bar)
    rbar.set_color("red")
    rbar.set_pos("-287, -386")

    bbar = Bar(bar)
    bbar.set_color("blue")
    bbar.set_pos("-187, -386")

    gbar = Bar(bar)
    gbar.set_color("green")
    gbar.set_pos("-87, -386")

    gbar2 = Bar(bar)
    gbar2.set_color("green")
    gbar2.set_pos("23, -386")

    scaler = SVG("g", 
                 rbar.bar, bbar.bar, gbar.bar, gbar2.bar,
                 transform="scale(0.5)")
    all = SVG("svg", filters, scaler)
    attr["height"] = 200
    attr["width"] = 300
    all.attr = attr
    all.save("all.svg")

if __name__ == "__main__":
    main()
