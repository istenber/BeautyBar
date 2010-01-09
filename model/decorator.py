#!/usr/bin/env python2.5

if __name__ == "__main__":
    import sys
    sys.path.append("/home/sankari/dev/beautybar")

import logging
from lib.svgfig import *
from StringIO import StringIO


class Decorator(object):

    def __init__(self, generator):
        self.generator = generator
        self.svg = load_stream(StringIO(self.generator.output()))
        self.width = 300 # TODO: read from svg
        self.height = 200 # TODO: read from svg

    def scale_str(self, scale_str):
        [x, y] = scale_str.split("x")
        if x is None or y is None:
            logging.error("# Incorrect scale string: " + scale_str)
            return None
        try:
            x = int(x) / 300
        except ValueError:
            x = 1
        try:
            y = int(y) / 200
        except ValueError:
            y = 1
        return self.scale_xy(x, y, False)
        
    def scale(self, scale):
        return self.scale_xy(scale, scale)

    def scale_xy(self, sx, sy, move=True):
        try:
            elem_id = self.svg[1]["id"]
            has_old = elem_id == "full_scaler"
        except KeyError:
            has_old = False
        if has_old:
            old_m = self.svg[1]["transform"][7:].split(",")
            old_sx = old_m[0]
            old_sy = old_m[3]
            sx = sx * float(old_sx)
            sy = sy * float(old_sy)
        if move:
            cx = float(self.svg.attr["width"]) * (1 - sx) / 2
            cy = float(self.svg.attr["height"]) * (1 - sy) / 2
        else:
            cx = 0
            cy = 0
        matrix = ("matrix(" + str(sx) + ", 0, 0, " + str(sy) +
                  ", " + str(cx) + ", " + str(cy) + ")")
        # logging.info("# scale/" + matrix)
        if has_old:
            self.svg[1]["transform"] = matrix
        else:
            scaler = SVG("g", id="full_scaler",
                         transform=matrix)
            for e in self.svg[1:]:
                scaler.append(e)
            self.svg[1] = scaler
            self.svg[2:] = ""
        self.width = 300 * sx
        self.height = 200 * sy
        self.svg.attr["width"] = self.width
        self.svg.attr["height"] = self.height

    def add_title(self, title):
        self.scale(0.8)
        bg_color = "ccffcc"
        title_bg = SVG("rect", x="50", y="0", width="200", height="20",
                       style="fill:#" + bg_color + ";stroke:#000000;")
        title_text = Text(x="60", y="15", d=title,
                          font_size=14,
                          text_align="center")
        title = SVG("g", title_bg, title_text.SVG())
        self.svg.append(title)

    def resize(self, width, height):
        w = float(self.svg.attr["width"])
        h = float(self.svg.attr["height"])
        self.scale_xy(width / w, height / h, move=False)
        self.svg.attr["width"] = width
        self.svg.attr["height"] = height

    def output(self):
        # self.scale(0.8)
        # self.add_title("hello")
        # self.resize(600, 200)
        return self.svg.standalone_xml()
        

def main():
    logging.getLogger().setLevel(logging.DEBUG)
    svg = """<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?>
<svg
   xmlns:svg=\"http://www.w3.org/2000/svg\"
   xmlns=\"http://www.w3.org/2000/svg\"
   width=\"100\"
   height=\"200\"
   id=\"svg_image\">
   <defs id=\"defs_id\"></defs>
   <rect
     y=\"20\" x=\"20\" height=\"20\" width=\"20\" id=\"rectangle1\"
     style=\"fill:#00ff00;\" />
   <rect
     y=\"40\" x=\"40\" height=\"30\" width=\"30\" id=\"rectangle2\"
     style=\"fill:#ffff00;\" />
   <rect
     y=\"50\" x=\"50\" height=\"10\" width=\"10\" id=\"rectangle2\"
     style=\"fill:#00ffff;\" />
</svg>

"""
    print Decorator(svg).output()

if __name__ == "__main__":
    main()
