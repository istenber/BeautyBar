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
        # TODO: change id!
    def set_color(self, color):
        if color == "red": return
        b = self.bar
        styles = (b[0], b[1, 0], b[1, 1], b[1, 2])
        if color == "blue": f = red_to_blue
        if color == "green": f = red_to_green
        for style in styles:
            f(style)    
    def set_pos(self, pos):
        x = -250+70*pos
        self.bar["transform"] = "translate(" + str(x) + ", -300)"
    def set_size(self, size):
        n = (5.9 * size)
        v = [n,
             600 - n,
             150 - n,
             620 - n]   
        self.bar[0]["height"] = v[0]
        self.bar[0]["y"] = v[1]
        self.bar[1,0]["height"] = v[0]
        self.bar[1,0]["y"] = v[1]
        self.bar[1,2]["transform"] = "translate(153," + str(v[2]) + ")"
        self.bar[1,1]["d"] = ("M 328, " + str(v[3]) + " L 328,600.79076")
        if size < 8: self._remove_ball_and_line()
    def _remove_ball_and_line(self):
        self.bar[1, 1] = ""
        self.bar[1, 2] = ""

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
    rbar.set_size(10)
    rbar.set_pos(1)

    bbar = Bar(bar)
    bbar.set_color("blue")
    bbar.set_size(20)
    bbar.set_pos(2)

    gbar = Bar(bar)
    gbar.set_color("green")
    gbar.set_size(30)
    gbar.set_pos(3)

    rbar2 = Bar(bar)
    rbar2.set_color("red")
    rbar2.set_size(40)
    rbar2.set_pos(4)

    bbar2 = Bar(bar)
    bbar2.set_color("blue")
    bbar2.set_size(45)
    bbar2.set_pos(5)

    gbar2 = Bar(bar)
    gbar2.set_color("green")
    gbar2.set_size(5)
    gbar2.set_pos(6)

    scaler = SVG("g", 
                 rbar.bar, bbar.bar, gbar.bar, 
                 rbar2.bar, bbar2.bar, gbar2.bar, 
                 transform="scale(0.5)")

    vertical_bar = SVG("path",
                       d="M 50,30 L 50,150",
                       style="stroke:#000000;stroke-width:1px")

    vertical_meter = SVG("g", 
                         vertical_bar)

    for val in range(0, 5):
        t = Text(20, 34+val*30, 
                 str(40-val*10), 
                 font_size=15).SVG()
        vertical_meter.append(t)

    horizontal_bar = SVG("path",
                         d="M 50,150 L 260,150",
                         style="stroke:#000000;stroke-width:1px")

    horizontal_meter = SVG("g", 
                           horizontal_bar)

    names = ["2000", "2001", "2002", "2003", "2004", "2005"]

    for val in range(0, 6):
        t = Text(58+val*35, 170,
                 names[val], 
                 font_size=10).SVG()
        horizontal_meter.append(t)

    meters = SVG("g",
                 vertical_meter,
                 horizontal_meter)                 

    all = SVG("svg", filters, meters, scaler)
    attr["height"] = 200
    attr["width"] = 300
    all.attr = attr
    all.save("all.svg")

if __name__ == "__main__":
    main()
