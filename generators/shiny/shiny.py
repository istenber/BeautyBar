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
        # -387, -386 is top corner
        if pos == 1: self._set_real_pos("-180, -300")
        if pos == 2: self._set_real_pos("-110, -300")
        if pos == 3: self._set_real_pos("-40, -300")
        if pos == 4: self._set_real_pos("30, -300")
        if pos == 5: self._set_real_pos("100, -300")
        if pos == 6: self._set_real_pos("170, -300")
    def _set_real_pos(self, pos):
        self.bar["transform"] = "translate(" + pos + ")"
    def set_size(self, size):

        v = [[100,
              498,
              48,
              519],
             [205,
              393,
              -58,
              419],
             ]
        self.bar[0]["height"] = v[size][0]
        self.bar[0]["y"] = v[size][1]
        self.bar[1,0]["height"] = v[size][0]
        self.bar[1,0]["y"] = v[size][1]
        # self.bar[1,2]["transform"] = "translate(153,-57.714286)"
        self.bar[1,2]["transform"] = "translate(153," + str(v[size][2]) + ")"

        # self.bar[1,1]["d"] = "M 328,419.36219 L 328,600.79076"
        self.bar[1,1]["d"] = ("M 328," + str(v[size][3]) + 
                              ".36219 L 328,600.79076")

    def _old(self):

        self.bar[0]["height"] = 100
        self.bar[0]["y"] = 498
        self.bar[1,0]["height"] = 100
        self.bar[1,0]["y"] = 498
        # self.bar[1,2]["transform"] = "translate(153,-57.714286)"
        self.bar[1,2]["transform"] = "translate(153," + "48" + ")"

        # self.bar[1,1]["d"] = "M 328,419.36219 L 328,600.79076"
        self.bar[1,1]["d"] = "M 328," + "519" + ".36219 L 328,600.79076"

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
    rbar.set_size(0)
    rbar.set_pos(1)

    bbar = Bar(bar)
    bbar.set_color("blue")
    bbar.set_size(1)
    bbar.set_pos(2)

    gbar = Bar(bar)
    gbar.set_color("green")
    gbar.set_size(0)
    gbar.set_pos(3)

    rbar2 = Bar(bar)
    rbar2.set_color("red")
    rbar2.set_pos(4)

    bbar2 = Bar(bar)
    bbar2.set_color("blue")
    bbar2.set_pos(5)

    gbar2 = Bar(bar)
    gbar2.set_color("green")
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
