import logging
import re

from lib.svgfig import *

from base import BaseGenerator
from attributes.common import Color

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

class Shiny(BaseGenerator):
    __red_bar = None

    def __init__(self):
        if Shiny.__red_bar is None:
            Shiny.__red_bar = load(template)
            # bar = svg[3, 0]
        self.attr = Shiny.__red_bar.attr
        self.colors = ["red", "blue", "green",
                       "red", "blue", "green"]
        self.bgcolor = "ffffff"
        self.screencolor = "ffffff"
        self.values = []

    def get_description(self):
        return ("Shiny diagram have nice shiny bars, but it is still " +
                "under heavy development.")

    def set_range(self, min, max):
        self.min = min
        self.max = max
    
    def add_row(self, name, value, index=None):
        self.values.append([name, value])

    def _append_bars(self, scaler):
        for index in range(0, 6):
            bar = Bar(Shiny.__red_bar[3, 0])
            bar.set_color(self.colors[index])
            bar.set_pos(index)
            f = 40.0 / (self.max - self.min)
            bar.set_size(self.values[index][1] * f)
            scaler.append(bar.bar)

    def _get_vertical_meter(self):
        vertical_bar = SVG("path",
                           d="M 50,30 L 50,150",
                           style="stroke:#000000;stroke-width:1px")
        vertical_meter = SVG("g", vertical_bar)
        s = 8
        step = (self.max - self.min) / (s - 1)
        for val in range(0, s):
            m = str(int(self.max-val*step))
            t = Text(20, 34+val*(120 / (s - 1)), m, font_size=13).SVG()
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

    def _get_sc(self):
        return SVG("rect", width=300, height=200, x=0, y=0, id="tausta_bg",
                   style="fill:#" + self.screencolor + ";")

    def _get_background(self):
        return SVG("rect", width=210, height=120, x=50, y=30, id="tausta_sc",
                   style="fill:#" + self.bgcolor + ";")

    def output(self):
        filters = Shiny.__red_bar[0]
        scaler = SVG("g", 
                 transform="scale(0.5)")
        self._append_bars(scaler)
        meters = self._get_meters()
        background = self._get_background()
        sc = self._get_sc()
        svg = SVG("svg", filters, sc, background, meters, scaler)
        svg.attr = Shiny.__red_bar.attr
        svg.attr["height"] = 200
        svg.attr["width"] = 300
        return svg.standalone_xml()

    def get_ui_name(self):
        return "Shiny bars"

    def get_attributes(self):
        bgcolor = Color(self, "bgcolor", "Background Color")
        screencolor = Color(self, "screencolor", "Screen Color")
        return [bgcolor, screencolor]
