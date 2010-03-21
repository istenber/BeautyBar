#!/usr/bin/env python

if __name__ == '__main__':
    import sys
    import os
    sys.path.append(os.path.abspath(os.path.dirname('..')))


from generators.__init__ import get_rating


class GuiInterface(object):
    """Interface to show diagram info for users.

    Different version have different capabilities:
     1. Support only datasets with six rows and fixed size 300x200
     2. Can have three to eight rows
    """

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
        for attr in self.get_attributes():
            if attr.get_name() == attribute: return attr
        return None

    def get_description(self):
        """Should return human readble description of generator"""
        return "no description"

    def get_version(self):
        """Get generator version"""
        return 1

    def get_rating(self):
        """Returns rating for chart. This is not chart property as is,
        but is useful to have here. One should NOT override this method"""
        return get_rating(self.get_name())


def main():
    from process_interface import tester
    import logging
    logging.getLogger().setLevel(logging.DEBUG)
    diagram = tester(
"""
Usage: ./generators/gui_interface.py <filename.py>
""")
    out = ("\nGuiInterface of \"" + diagram.get_ui_name() + "\" (" +
           diagram.get_name() + "):\n" +
           "[ Interface version: " + str(diagram.get_version()) +
           " - Rating : " + str(diagram.get_rating()) + " ]\n" +
           "---------------------------------------\n" +
           diagram.get_description() + "\n" +
           "---------------------------------------\n")
    for attr in diagram.get_attributes():
        out += attr.get_ui_name() + " : " + attr.get_type() + "\n"
    out += "---------------------------------------\n"
    print out


if __name__ == "__main__":
    main()
