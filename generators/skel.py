#!/usr/bin/env python

from gui_interface import GuiInterface

class Empty(GuiInterface):
    def name(self):
        return "Empty generator"
    
    def attributes(self):
        return []

def main():
    e = Empty()
    print "name -> " + e.name()

if __name__ == "__main__":
    main()
