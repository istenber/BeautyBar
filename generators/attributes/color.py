from attribute import Attribute

class Color(Attribute):
    def __init__(self, x_name, name, setter, getter):
        self._x_name = x_name
        self._name = name
        self.s = setter
        self.g = getter
    def set(self, color):
        self.s(color)
    def get(self):
        return self.g()
    def name(self):
        return self._name
    def x_name(self):
        return self._x_name
    def type(self):
        return "Color"
