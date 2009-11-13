#!/usr/bin/env python

# TODO: remove!
if __name__ == "__main__":
    import sys
    LIB_PATH = "/home/sankari/dev/beautybar/"
    sys.path.append(LIB_PATH)

import logging
import re

from lib.svgfig import *

from gui_interface import GuiInterface

template="generators/shiny/red.svg"

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
        x = -250+70*(pos+1)
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
        self.bar[1,1]["d"] = ("M 328," + str(v[3]) + " L 328,600.79076")
        if size < 8: self._remove_ball_and_line()
    def _remove_ball_and_line(self):
        self.bar[1, 1] = ""
        self.bar[1, 2] = ""

class Shiny(GuiInterface):
    __red_bar = None

    def __init__(self):
        if Shiny.__red_bar is None:
            Shiny.__red_bar = load(template)
            # bar = svg[3, 0]
        self.attr = Shiny.__red_bar.attr
        self.colors = ["red", "blue", "green",
                       "red", "blue", "green"]
        self.values = []

    def scale(self, min, max):
        # TODO: some functionality?
        pass
    
    def add(self, name, value):
        self.values.append([name, value])

    def _append_bars(self, scaler):
        for index in range(0, 6):
            bar = Bar(Shiny.__red_bar[3, 0])
            bar.set_color(self.colors[index])
            bar.set_pos(index)
            bar.set_size(self.values[index][1])
            scaler.append(bar.bar)

    def _get_vertical_meter(self):
        vertical_bar = SVG("path",
                           d="M 50,30 L 50,150",
                           style="stroke:#000000;stroke-width:1px")
        vertical_meter = SVG("g", vertical_bar)
        for val in range(0, 5):
            t = Text(20, 34+val*30, 
                     str(40-val*10), 
                     font_size=15).SVG()
            vertical_meter.append(t)
        return vertical_meter

    def _get_horizontal_meter(self):
        horizontal_bar = SVG("path",
                             d="M 50,150 L 260,150",
                             style="stroke:#000000;stroke-width:1px")        
        horizontal_meter = SVG("g", horizontal_bar)
        for val in range(0, 6):
            t = Text(58+val*35, 170,
                     self.values[val][0],
                     font_size=10).SVG()
            horizontal_meter.append(t)
        return horizontal_meter

    def _get_meters(self):
        return SVG("g",
                   self._get_vertical_meter(),
                   self._get_horizontal_meter())

    def output(self):
        filters = Shiny.__red_bar[0]
        scaler = SVG("g", 
                 transform="scale(0.5)")
        self._append_bars(scaler)
        meters = self._get_meters()
        svg = SVG("svg", filters, meters, scaler)
        svg.attr = Shiny.__red_bar.attr
        svg.attr["height"] = 200
        svg.attr["width"] = 300
        # return "" 
        return svg.standalone_xml()

    def name(self):
        return "Shiny bars"
    
    def attributes(self):
        return []

    def disabled(self):
        return False


def main():
    logging.getLogger().setLevel(logging.DEBUG)
    bars = Shiny()
    bars.scale(0, 50)
    bars.add("Ilpo", 28)
    bars.add("Lasse", 24)
    bars.add("Sanna", 27)
    bars.add("Ilpo", 28)
    bars.add("Lasse", 24)
    bars.add("Sanna", 27)
    print bars.output()

if __name__ == "__main__":
    main()
