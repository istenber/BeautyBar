import logging

from base import BaseGenerator

class Skel(BaseGenerator):
    def __init__(self):
        pass

    # Process interface
    def set_range(self, min, max):
        pass
    def add_row(self, name, value, index):
        pass
    def output(self):
        pass

    # Gui interface
    def get_description(self):
        pass
    def get_ui_name(self):
        pass
    def get_attributes(self):
        pass
    def get_rating(self):
        pass
