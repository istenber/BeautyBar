#!/usr/bin/env python

import logging

from xml.dom import minidom

from gui_interface import GuiInterface
from attributes.bgcolor import BgColor

# TODO: read path with some other way?
template="generators/houses/base.svg"
houses_template="generators/houses/all-houses.svg"

class House(object):
    def parse(self):
        self.doc = minidom.parse(houses_template)
        self._elem(self.doc)

    def outme(self, elem):
        print "found: " + str(elem.getAttribute("id"))
        print "" + elem.toprettyxml() + "\n\n"

    def _elem(self, elem):
        # print "elem: " + str(elem.nodeValue)
        try:
            id = elem.getAttribute("id")
            if id.startswith("house"):
                self.outme(elem)
        except AttributeError:
            pass
        for child in elem.childNodes:
            self._elem(child)

class Houses(GuiInterface):

    def __init__(self):
        self.values = []
        # TODO: change to english
        self.id_prefixes = [ "arvo", "aika" ]
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
        logging.info(self._debug_values())
        
    def _debug_values(self):
        out = "saving ("
        for v in self.values:
            out += str(v) + ","
        out = out[:-1] + ")"
        return out

    def name(self):
        return "House bars"
    
    def attributes(self):
        return [BgColor()]

    def disabled(self):
        return True

def main():
    logging.getLogger().setLevel(logging.DEBUG)
    house = House()
    house.parse()

def xxx():
    houses = Houses()
    houses.scale(0, 50)
    houses.add("small", 10)
    houses.add("large", 48)
    houses.add("largetoo", 47)
    houses.add("smalltoo", 12)
    houses.add("medium", 23)
    houses.add("last", 33)
    print houses.output()

if __name__ == "__main__":
    main()
