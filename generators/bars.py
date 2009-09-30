#!/usr/bin/env python

from lxml import etree

template="bars/template.svg"

class Bars(object):
    def __init__(self):
        self.values = []
        self.id_prefixes = [ "tarkka", "arvo", "aika", "pylvas" ]
    def scale(self, scale):
        self.scale = scale
    def add(self, name, value):
        self.values.append([name, value])
    def output(self, filename):
        self.tree = etree.parse(template)
        self._generate_output()        
        with open(filename, 'w') as f:
           f.write(self.output)
        # self._debug()

    def _process_pylvas(self, index, elem):
        # TODO:
        print "# process_pylvas: " + str(elem)

    def _process_aika(self, index, elem):
        # print "# process_aika: " + str(elem)
        tspan = elem.getchildren()[0]
        tspan.text = str(self.values[index][0])

    def _process_tarkka(self, index, elem):
        # print "# process_tarkka: " + str(elem)
        tspan = elem.getchildren()[0]
        tspan.text = str(self.values[index][1])

    def _process_arvo(self, index, elem):
        # print "# process_arvo: " + str(elem)
        tspan = elem.getchildren()[0]
        tspan.text = str(self.scale[index])

    def _generate_output(self):
        for elem in self.tree.iter():
            id = elem.get("id")
            for id_prefix in self.id_prefixes:
                if id.startswith(id_prefix):
                    func = "_process_" + id_prefix
                    index = int(str(elem.get("id"))[len(id_prefix):])
                    print ("# Calling self." + str(func) + "(" + str(index) +
                           ", <Element...>)")
                    self.__getattribute__(func)(index, elem)

        self.output = etree.tostring(self.tree)

    def _read_template(self):
        self.template = ""
        with open(template, 'r') as f:
            self.template = f.read()

    def _debug(self):
        for value in self.values:
            print "val: " + str(value)
        for s in self.scale:
            print "s: " + str(s)
        # print "tmplate\n" + str(self.output)
        # for action, elem in self.tree.iter():
            # print "act: " + str(action) + "\telem: " + str(elem)
        for elem in self.tree.iter():
            print "elem: " + str(elem)
            for key in elem.keys():
                print "\tkey: " + str(key) + "\t-> " + str(elem.get(key))

def main():
    bars = Bars()
    bars.scale([0, 10, 20, 30, 40, 50])
    bars.add("Ilpo", 28)
    bars.add("Lasse", 24)
    bars.add("Sanna", 27)
    bars.add("Ilpo", 28)
    bars.add("Lasse", 24)
    bars.add("Sanna", 27)
    bars.output("/tmp/bars_test.svg")

if __name__ == "__main__":
    main()
