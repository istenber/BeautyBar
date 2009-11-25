#!/usr/bin/env python

import logging

from xml.dom import minidom

from gui_interface import GuiInterface
from attributes.color import Color

# TODO: read path with some other way?
template="generators/bars/template.svg"

class Bars(GuiInterface):

    def __init__(self):
        self.values = []
        # TODO: change to english
        self.id_prefixes = [ "arvo", "aika", "pylvas", "tausta" ]
        self.bg_color = "0000ff"
        self.bar_color = "ff0000"
    def scale(self, min, max):
        self.step = (max - min) / 5
        self.scale = range(min, max + self.step, self.step)
        # print "# scale " + str(self.scale)
    def add(self, name, value):
        self.values.append([name, value])
    def output(self):
        self.doc = minidom.parse(template)
        self._generate_output()        
        return self.output
        # with open("/tmp/bars_output.svg", 'w') as f:
        #     f.write(self.output)
        # self._debug()

    def _process_tausta(self, index, elem):
        style = elem.getAttribute("style")
        ns = style.replace("fill:#0000ff;", "fill:#" + self.bg_color + ";")
        elem.setAttribute("style", ns)
    # 1 = 3.2 pixel
    def _process_pylvas(self, index, elem):
        # print "# process_pylvas: " + str(elem)
        # y = 435 - (int(self.values[index][1]) * self.step * 73 / 100)
        # h = 433 - y
        h = int(self.values[index][1]) * 3.2
        y = 177 - h
        # print "\ty: " + str(y)
        # print "\th: " + str(h)
        elem.setAttribute("height", str(h))
        elem.setAttribute("y", str(y))
        style = elem.getAttribute("style")
        ns = style.replace("fill:#ff0000;", "fill:#" + self.bar_color + ";")
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
        new_txt = self.doc.createTextNode(str(self.scale[index]))
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

    def _set_bg(self, color):
        self.bg_color = color

    def _get_bg(self):
        return self.bg_color

    def _set_barc(self, color):
        self.bar_color = "00ff00"
        # TODO: enable self.bar_color = color

    def _get_barc(self):
        return self.bar_color

    def name(self):
        return "Simple bars"
    
    def attributes(self):
        bg_color = Color("bgcolor", "Background Color", 
                         self._set_bg, self._get_bg)
        bar_color = Color("barcolor", "Color of bars",
                          self._set_barc, self._get_barc)
        return [bg_color, bar_color]

    def disabled(self):
        return False

def main():
    logging.getLogger().setLevel(logging.DEBUG)
    bars = Bars()
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
