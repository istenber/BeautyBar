#!/usr/bin/env python2.5

import tempfile
from svgfig import *


# --------------------------------------------------------
#   Defaults
# --------------------------------------------------------

TMP_PATH = ''

SVG_DEFAULTS = {
    'height'   : "200px",
    'width'    : "300px",
    'tmp_path' : tempfile.mkdtemp(),
    }


# --------------------------------------------------------
#   Helpers
# --------------------------------------------------------

def make_svg(filename, data, **attr):    
    svg_attr = dict(SVG_DEFAULTS)
    svg_attr.update(attr)
    svg = SVG("svg", data)
    svg.attr['height'] = svg_attr['height']
    svg.attr['width'] = svg_attr['width']
    svg.attr['xmlns'] = "http://www.w3.org/2000/svg"
    svg.attr['xmlns:svg'] = "http://www.w3.org/2000/svg"
    svg.attr['xmlns:xlink'] = "http://www.w3.org/1999/xlink"
    filename = svg_attr['tmp_path'] + "/" + filename
    try:
        f = open(filename, "w")
    except IOError:
        return
    print "eog", filename
    f.write(svg.standalone_xml())
    f.close()


# --------------------------------------------------------
#   Tests
# --------------------------------------------------------

def run_tests():
    test_grid()
    test_box_grid()


def test_grid():
    g = SVG("g")
    g.append(Rect(0, 0, 300, 200, style="fill:#ffffff;").SVG())
    g.append(Rect(0, 20, 300, 160, style="fill:#ff0000;").SVG())
    g.append(gs.Grid(min_level = 160,
                     max_level = 20,
                     line_height = 2,
                     line_count = 8,
                     color = "800000",
                     has_bline = False).SVG())
    make_svg("grid_test.svg", g)

def test_box_grid():
    g = SVG("g")
    g.append(Rect(0, 0, 300, 200, style="fill:#0000ff;").SVG())
    g.append(Rect(0, 20, 300, 160, style="fill:#ff0000;").SVG())
    g.append(gs.BoxGrid(min_level = 160,
                        max_level = 20).SVG())
    make_svg("box_grid_test.svg", g)


# --------------------------------------------------------

if __name__ == "__main__":
    run_tests()
