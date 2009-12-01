#!/usr/bin/env python


class GuiInterface(object):
    """Interface to show diagram info for users."""

    def __init__(self):
        if self.__class__ is GuiInterface:
            raise NotImplementedError

    def get_name(self):
        """Should return computer usable name for diagram"""
        return self.__class__.__name__.lower()

    def get_ui_name(self):
        """Should return human readble name of diagram"""
        return self.__class__.__name__

    def get_attributes(self):
        """Should return list of all attributes that diagram can take"""
        return []

    def get_attribute(self, attribute):
        """Should return value of attribute"""
        return None


def main():

    def get_info(diagram):
        out = ("\nGuiInterface of \"" + diagram.get_ui_name() + "\" (" +
               diagram.get_name() + ")\n" +
               "---------------------------------------\n")
        for attr in diagram.get_attributes():
            out += attr.name() + " : " + attr.type() + "\n"
        out += "---------------------------------------\n"
        return out

    from process_interface import tester
    diagram = tester("gui_interface.py")
    print get_info(diagram)

if __name__ == "__main__":
    main()
