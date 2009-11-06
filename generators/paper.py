#!/usr/bin/env python

import logging

from xml.dom import minidom

from gui_interface import GuiInterface
from attributes.bgcolor import BgColor

# TODO: read path with some other way?
template="generators/paper/template.svg"

class Paper(GuiInterface):

    def __init__(self):
        self.values = []
        # TODO: change to english
        self.id_prefixes = [ "arvo", "nimi", "pylvas" ]
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

    def _process_pylvas(self, index, elem):
        y_table = [ 1.4, 39, 78.4, 117.6, 156.8, 196 ]
        # logging.info("# process_pylvas: " + str(elem))
        v = int(self.values[index][1]) / 10.0
        #tr = elem.getAttribute("transform")
        #logging.info("## tr b4:" + str(tr))
        s = v * 0.25 + 0.01
        y = y_table[index]
        x = (4 - v) * 43 - 3
        elem.setAttribute("transform", 
                          "matrix(1,0,0," + (str(s) + "," + 
                                             str(y) + "," +
                                             str(x) + ")"))
    def _process_nimi(self, index, elem):
        # print "# process_nimi: " + str(elem)
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
        return "Paper bars"
    
    def attributes(self):
        return [BgColor()]

def main():
    logging.getLogger().setLevel(logging.DEBUG)
    paper = Paper()
    paper.scale(0, 50)
    paper.add("Ilpo", 28)
    paper.add("Lasse", 24)
    paper.add("Sanna", 27)
    paper.add("Ilpo", 28)
    paper.add("Lasse", 24)
    paper.add("Sanna", 27)
    print paper.output()

if __name__ == "__main__":
    main()
