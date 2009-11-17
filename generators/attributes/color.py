from attribute import Attribute

class Color(Attribute):
    def __init__(self, text, callback):
        self.text = text
        self.callback = callback
    def name(self):
        return self.text
    def type(self):
        return "Color"
