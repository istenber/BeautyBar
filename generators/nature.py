import logging

from base import BaseGenerator

from lib.svgfig import *

# TODO: use some other kind of url
# img="/home/sankari/dev/beautybar/doc/generator_design/ideas/nature-1.jpg"
img="/images/nature-1.jpg"

class SvgFigGenerator(BaseGenerator):

    def __init__(self):
        self.rows = []
    
    def output(self):
        svg = SVG("svg")
        svg.append(self.get_defs())
        svg.append(self.get_elements())
        svg.attr["height"] = "200px"
        svg.attr["width"] = "300px"
        svg.attr["xmlns"] = "http://www.w3.org/2000/svg"
        svg.attr["xmlns:svg"] = "http://www.w3.org/2000/svg"
        svg.attr["xmlns:xlink"] = "http://www.w3.org/1999/xlink"
        return svg.standalone_xml()

    def set_range(self, min, max):
        # TODO: range
        pass

    def add_row(self, name, value, index=None):
        self.rows.append([name, value])


class Nature(SvgFigGenerator):

    def get_defs(self):
        # TODO: not used!
        #r = SVG("rect", id="bgrect",
        #        height=200, width=200, x=0, y=0)
        #cp = SVG("clipPath", r, id="bgimage")
        #defs = SVG("defs", cp, id="defs")
        defs = SVG("defs", id="defs")
        return defs

    def get_elements(self):
        return SVG("g", 
                   self._get_background(),
                   self._get_bars())

    def _get_background(self):
        # bg colors are black and green, and we get roundings by using
        # stroke and stroke-linejoin:round
        shadow_style=("stroke:#000000;stroke-width:50;stroke-linejoin:round;")
        bg_style=("stroke:#00aa00;stroke-width:50;stroke-linejoin:round;" +
                  "fill:#00aa00;")
        bg = SVG("g",
                 # shadow is box from 10, 10 to bottom corner, as it
                 # uses stroke width 50 (25 for both sides) based on
                 # place 35 (=25+10)
                 SVG("rect", id="bg_shadow", x=35, y=35,
                     width=240, height=140, style=shadow_style),
                 # color is same as shadow but move a bit
                 SVG("rect", id="bg_color", x=25, y=25,
                     width=240, height=140, style=bg_style),
                 # in middle we have black screen where all data will come
                 # it is not shown, but only top and bottom lines
                 # width could be 290, but just to have some error margin
                 SVG("rect", id="bg_frame", x=0, y=25,
                     width=292, height=140, style="fill:#000000;"),
                 # image is a bit smaller (2px from top and 2px from bottom)
                 # than frame and it leaves only small part of frame visible
                 SVG("image", id="bg_image",x=0, y=27,
                     width=290, height=136,
                     xlink__href=img))
        # TODO: modify image to correct size!!
        # image size 290x136
        # TODO: fix image href
        return bg

    def _get_bars(self):
        bars = SVG("g")
        # TODO: refactor names
        # TODO: calculate x axis places
        # (290-40*6-10)/2 = 30
        # full_width-bar_size_with_space*bar_count-last_bar_space
        # divided by to as we want same amount of space both sides
        i = 30
        bar_width=30
        shs = 3
        for row in self.rows:
            name = str(row[0])
            # TODO: scale value (50.0 -> to something else)
            # 140 is max value that fits in frame, maybe we need
            # a bit smaller... and shadows take space as well
            value = row[1] * 135.0 / 50.0
            # baseline is at 165 (=200-10-25)
            pos = 165-value
            bar = SVG("g",
                      SVG("rect", id="shadow_" + name, width=bar_width, x=i-shs,
                          height=value+shs, y=pos-shs,
                          style="fill:#000000"),
                      SVG("rect", id="bar_" + name, width=bar_width, x=i,
                          y=pos, height=value,
                          style="fill:#00ff00"),
                      Text(i+bar_width/2.0, 180, name, font_size=11,
                           style="fill:#00ff00; text-anchor:middle;").SVG())
            # TODO: center text!
            bars.append(bar)
            i += 40
        return bars

    # Gui interface
    def get_description(self):
        return "Theme from nature"
    def get_ui_name(self):
        return "Nature theme"
    def get_attributes(self):
        # TODO: allow changing picture
        # TODO: allow color themes
        # TODO: different size and placed shadows for bars
        # TODO: font size
        return []
    def get_rating(self):
        return 5
