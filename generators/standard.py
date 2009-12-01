import logging

from xml.dom import minidom

from base import BaseGenerator
from attributes.common import Color, Boolean

# TODO: read path with some other way?
template="generators/standard/template.svg"

class Standard(BaseGenerator):

    def __init__(self):
        self.values = []
        # TODO: change to english
        self.id_prefixes = [ "arvo", "aika", "pylvas", "tausta", "grid" ]
        self.bgcolor = "0000ff"
        self.barcolor = "ff0000"
        self.has_grid = True
        self.min = 0
        self.step = 1
    def set_range(self, min, max):
        self.step = (max - min) / 50.0
        self.min = min
        # logging.info("### step size: " + str(self.step))
        self.scale_meter = range(int(min),
                                 int(max + self.step * 10),
                                 int(self.step * 10))
        # print "# scale " + str(self.scale)
    def add_row(self, name, value, index=None):
        self.values.append([name, value])
    def output(self):
        self.doc = minidom.parse(template)
        self._generate_output()        
        return self.output
        # with open("/tmp/bars_output.svg", 'w') as f:
        #     f.write(self.output)
        # self._debug()
    def _process_grid(self, index, elem):
        if self.has_grid: return
        p = elem.parentNode
        p.removeChild(elem)
    def _process_tausta(self, index, elem):
        style = elem.getAttribute("style")
        ns = style.replace("fill:#0000ff;", "fill:#" + self.bgcolor + ";")
        elem.setAttribute("style", ns)
    # 1 = 3.2 pixel
    def _process_pylvas(self, index, elem):
        # print "# process_pylvas: " + str(elem)
        # y = 435 - (int(self.values[index][1]) * self.step * 73 / 100)
        # h = 433 - y
        value = float(self.values[index][1]) - self.min
        h = value * 3.2 / self.step
        y = 177 - h
        # print "\ty: " + str(y)
        # print "\th: " + str(h)
        elem.setAttribute("height", str(h))
        elem.setAttribute("y", str(y))
        style = elem.getAttribute("style")
        ns = style.replace("fill:#ff0000;", "fill:#" + self.barcolor + ";")
        elem.setAttribute("style", ns)
    def _process_aika(self, index, elem):
        # print "# process_aika: " + str(elem)
        tspan = elem.childNodes[0]
        old_txt = tspan.childNodes[0]
        new_txt = self.doc.createTextNode(str(self.values[index][0]))
        tspan.replaceChild(new_txt, old_txt)
    def _process_arvo(self, index, elem):
        # print "# process_arvo: " + str(elem)
        tspan = elem.childNodes[0]
        old_txt = tspan.childNodes[0]
        new_txt = self.doc.createTextNode(str(self.scale_meter[index]))
        tspan.replaceChild(new_txt, old_txt)
    def _elem(self, elem):
        # print "elem: " + str(elem.nodeValue)
        try:
            id = elem.getAttribute("id")
            for id_prefix in self.id_prefixes:
                if id.startswith(id_prefix):
                    func = "_process_" + id_prefix
                    index = int(id[len(id_prefix):])
                    # print ("# Calling self." + str(func) + "(" + str(index) +
                    #        ", <Element...>)")
                    self.__getattribute__(func)(index, elem)
        except AttributeError:
            pass
        for child in elem.childNodes:
            self._elem(child)

    def _generate_output(self):
        self._elem(self.doc)
        self.output = self.doc.toprettyxml()
        # logging.info(self._debug_values())
        
    def _debug_values(self):
        out = "saving ("
        for v in self.values:
            out += str(v) + ","
        out = out[:-1] + ")"
        return out

    def get_ui_name(self):
        return "Simple bars"
    
    def get_attributes(self):
        bgcolor = Color(self, "bgcolor", "Background Color")
        barcolor = Color(self, "barcolor", "Color of bars")
        has_grid = Boolean(self, "has_grid", "Grid")
        return [bgcolor, barcolor, has_grid]
