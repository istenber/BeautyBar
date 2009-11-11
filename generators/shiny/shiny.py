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
    def _sub_func(c):
        pass
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

def blue_to_green(style):
    convert_color(style, lambda c: c[1:3] + c[5:7] + c[3:5])

def red_to_blue(style):
    convert_color(style, lambda c: c[5:7] + c[3:5] + c[1:3])

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
    styles = (bar[0], bar[1, 0], bar[1, 1], bar[1, 2])
    # print str(bar)
    rbar = bar.clone()

    for style in styles:
        red_to_blue(style)
    svg.save("blue.svg")
    bbar = bar.clone()

    for style in styles:
        blue_to_green(style)
    svg.save("green.svg")
    gbar = bar.clone()

    # print "r: " + str(rbar)
    # print "g: " + str(bbar)
    # print "b: " + str(gbar)

    rbar["transform"] = "translate(-287,-386)"
    bbar["transform"] = "translate(-187,-386)"
    gbar["transform"] = "translate(-87,-386)"

    scaler = SVG("g", rbar, bbar, gbar, transform="scale(0.5)")

    # all = SVG("svg", filters, rbar, bbar, gbar)
    all = SVG("svg", filters, scaler)
    # print attr
    attr["height"] = 200
    attr["width"] = 300
    all.attr = attr
    all.save("all.svg")

if __name__ == "__main__":
    main()
