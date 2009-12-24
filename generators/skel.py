import logging

from base import BaseGenerator

class Skel(BaseGenerator):
    def __init__(self):
        pass

    # Process interface
    def set_range(self, min, max):
        pass
    def add_row(self, name, value, index=None):
        pass
    def output(self):
        return ""

    # Gui interface
    def get_description(self):
        return ""
    def get_ui_name(self):
        return ""
    def get_attributes(self):
        return []
    def get_rating(self):
        return 1
