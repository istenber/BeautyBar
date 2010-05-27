import logging
import svgfig


__all__ = ['Grid', 'BoxGrid']


GRID_DEFAULTS = {
    'min_level'     : 180,
    'max_level'     : 20,
    'line_count'    : 6,
    'line_x0'       : 10,
    'line_height'   : 2,
    'bline_x0'      : 0,
    'bline_height'  : 3,
    'color'         : "000000",
    'has_bline'     : True,
    }


class Grid(object):

    def __init__(self, **attr):
        self.attr = dict(GRID_DEFAULTS)
        self.attr.update(attr)

    def SVG(self):
        g = svgfig.SVG("g")
        a = self.attr
        line_width = 300 - 2 * a['line_x0']
        if a['has_bline']:
            bline_width = 300 - 2 * a['bline_x0']
            g.append(svgfig.SVG("rect",
                                x = a['bline_x0'], width = bline_width,
                                y = a['min_level'], height = a['bline_height'],
                                style="fill:#%s;" % a['color']))
        k = (a['min_level'] - a['max_level']) / (a['line_count'] - 1)
        for i in range(1, a['line_count']):
            y = a['min_level'] - i * k
            g.append(svgfig.SVG("rect",
                                x = a['line_x0'], width = line_width,
                                y = y, height = a['line_height'],
                                style="fill:#%s;" % a['color']))
        return g


BOX_GRID_DEFAULTS = {
    'color1'     : "cccccc",
    'color2'     : "ffffff",
    'box_count'  : 5,
    }


class BoxGrid(Grid):

    def __init__(self, **attr):
        self.attr = dict(GRID_DEFAULTS)
        self.attr.update(BOX_GRID_DEFAULTS)
        self.attr.update(attr)

    def SVG(self):
        g = svgfig.SVG("g")
        a = self.attr
        line_width = 300 - 2 * a['line_x0']
        if a['has_bline']:
            bline_width = 300 - 2 * a['bline_x0']
            g.append(svgfig.SVG("rect",
                                x = a['bline_x0'], width = bline_width,
                                y = a['min_level'], height = a['bline_height'],
                                style="fill:#%s;" % a['color']))
        k = (a['min_level'] - a['max_level']) / a['box_count']
        for i in range(1, a['box_count'] + 1):
            y = a['min_level'] - i * k
            if i % 2 == 0:
                color = a['color1']
            else:
                color = a['color2']
            g.append(svgfig.SVG("rect",
                                x = a['line_x0'], width = line_width,
                                y = y, height = k,
                                style="fill:#%s;" % color))
        return g
