import logging

from svgfig_base import SvgFigGenerator
from attributes.common import Color, Boolean, Choice

from lib.svgfig import *


class Errormsg(SvgFigGenerator):

    def set_msg(self, msg):
        self.msg = msg

    def get_elements(self):
        return Text(150, 100, self.msg, font_size=15,
                    style="fill:#000000;text-anchor:middle;").SVG()

    def get_description(self):
        return ""

    def get_ui_name(self):
        return ""

    def get_attributes(self):
        return []

    def get_version(self):
        return 1
