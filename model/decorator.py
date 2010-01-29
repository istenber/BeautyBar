#!/usr/bin/env python2.5

if __name__ == "__main__":
    import sys
    sys.path.append("/home/sankari/dev/beautybar")

import logging
from lib.svgfig import *
from cStringIO import StringIO


class Decorator(object):

    def __init__(self, generator):
        self.generator = generator
        # needed if cStringIO is used
        utf16_str = self.generator.output().encode("UTF-16")
        self.svg = load_stream(StringIO(utf16_str))
        self.width = self._to_pixels(self.svg.attr['width'])
        self.height = self._to_pixels(self.svg.attr['height'])

    def _to_pixels(self, string):
        if "px" in string:
            string = string.replace("px", "")
        try:
            return float(string)
        except ValueError:
            return 0

    def resize_str(self, resize_str):
        """Get new image size as string: \"300x200\""""
        try:
            [x, y] = resize_str.split("x")
        except ValueError:
            logging.error("Incorrect resize string: " + resize_str)
            return
        try:
            x = int(x)
            y = int(y)
        except ValueError:
            return None
        return self.resize(x, y)
        
    def scale(self, scale):
        return self.scale_xy(scale, scale)

    def _done_before(self):
        if not hasattr(self, "_db_flag"):
            try:
                self._db_flag = (self.svg[self._ip()]["id"] == "full_scaler")
            except KeyError:
                self._db_flag = False
        return self._db_flag

    def _ip(self): # items position, defs + 1
        if not hasattr(self, "_ipos_flag"):
            if self.svg[0].t == "defs":
                self._ipos_flag = 1
            else:
                self._ipos_flag = 0
        return self._ipos_flag

    def scale_xy(self, sx, sy, move=True):
        """We can scale x axis and y axis different amount, and
        we might want to move figure to center after scaling"""
        if self._done_before():
            old_matrix = self.svg[self._ip()]["transform"][7:].split(",")
            sx = sx * float(old_matrix[0])
            sy = sy * float(old_matrix[3])
        if move:
            cx = self.width * (1 - sx) / 2
            cy = self.height * (1 - sy) / 2
        else:
            cx = 0
            cy = 0
        matrix = ("matrix(" + str(sx) + ", 0, 0, " + str(sy) +
                  ", " + str(cx) + ", " + str(cy) + ")")
        # logging.info("# scale/" + matrix)
        if self._done_before():
            self.svg[self._ip()]["transform"] = matrix
        else:
            scaler = SVG("g", id="full_scaler", transform=matrix)
            for e in self.svg[self._ip():]:
                scaler.append(e)
            self.svg[self._ip()] = scaler
            self.svg[(self._ip() + 1):] = ""
        self.width = 300 * sx
        self.height = 200 * sy

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
        self.scale_xy(width / self.width, height / self.height, move=False)

    def output(self):
        # self.scale(0.8)
        # self.add_title("hello")
        # self.resize(600, 200)
        self.svg.attr["width"] = self.width
        self.svg.attr["height"] = self.height
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
