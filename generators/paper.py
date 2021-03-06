import logging

from xml.dom import minidom
from base import BaseGenerator
from attributes.common import Color, Float

# TODO: read path with some other way?
template="generators/paper/template.svg"

class Paper(BaseGenerator):

    def __init__(self):
        self.values = []
        # TODO: change to english
        self.id_prefixes = [ "arvo", "nimi", "pylvas", "viiva", "praja"]
        self.linecolor = "000000"
        self.linesize = 1.0
    def get_description(self):
        return "This diagram looks like paper."
    def set_range(self, min, max):
        self.step = (max - min) / 50.0
        self.min = min
        self.scale = range(int(min),
                           int(max + self.step * 10),
                           int(self.step * 10))
        # print "# scale " + str(self.scale)
    def add_row(self, name, value, index=None):
        self.values.append([name, value])
    def output(self):
        self.doc = minidom.parse(template)
        self._generate_output()        
        return self.output
    def _line_size(self, elem):
        style = elem.getAttribute("style")
        ns = style.replace("stroke-width:1.0px;",
                           "stroke-width:" + str(self.linesize) + "px;")
        elem.setAttribute("style", ns)
    def _line_color(self, elem, color_elem):
        style = elem.getAttribute("style")
        ns = style.replace(color_elem + ":#000000;",
                           color_elem + ":#" + self.linecolor + ";")
        elem.setAttribute("style", ns)
    def _process_viiva(self, index, elem):
        self._line_color(elem, "stroke")
        self._line_size(elem)
    def _process_pylvas(self, index, elem):
        y_table = [ 1.4, 39, 78.4, 117.6, 156.8, 196 ]
        # logging.info("# process_pylvas: " + str(elem))
        v = (self.values[index][1] - self.min) / (10 * self.step)
        #tr = elem.getAttribute("transform")
        #logging.info("## tr b4:" + str(tr))
        s = v * 0.25 + 0.01
        y = y_table[index]
        x = (4 - v) * 43 - 3
        elem.setAttribute("transform", 
                          "matrix(1,0,0," + (str(s) + "," + 
                                             str(y) + "," +
                                             str(x) + ")"))
    def _process_praja(self, index, elem):
        self._line_color(elem, "stroke")
        self._line_size(elem)
    def _process_nimi(self, index, elem):
        # print "# process_nimi: " + str(elem)
        tspan = elem.childNodes[0]
        old_txt = tspan.childNodes[0]
        new_txt = self.doc.createTextNode(str(self.values[index][0]))
        tspan.replaceChild(new_txt, old_txt)
        self._line_color(elem, "fill")
    def _process_arvo(self, index, elem):
        # print "# process_arvo: " + str(elem)
        tspan = elem.childNodes[0]
        old_txt = tspan.childNodes[0]
        new_txt = self.doc.createTextNode(str(self.scale[index]))
        tspan.replaceChild(new_txt, old_txt)
        self._line_color(elem, "fill")
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

    def get_ui_name(self):
        return "Paper bars"
    
    def get_attributes(self):
        linecolor = Color(self, "linecolor", "Line color")
        linesize = Float(self, "linesize", "Line size", 0.1, 2.0)
        return [linecolor, linesize]
