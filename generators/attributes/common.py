from attribute import Attribute

# TODO: add validators... or something?

class Color(Attribute):

    def value_to_string(self, value):
        return value

    def string_to_value(self, string):
        if len(string) == 6: return string
        return "ffffff"


class Boolean(Attribute):

    def value_to_string(self, value):
        if value: return "true"
        return "false"

    def string_to_value(self, string):
        if string == "true": return True
        return False


class Choice(Attribute):

    def __init__(self, generator, name, ui_name, choices):
        Attribute.__init__(self, generator, name, ui_name)
        self.choices = choices

    def value_to_string(self, value):
        return str(value)

    def string_to_value(self, string):
        return int(string)


class Float(Attribute):

    def __init__(self, generator, name, ui_name, min, max):
        Attribute.__init__(self, generator, name, ui_name)
        if min is None: min = 0.0
        if max is None: max = 10.0
        self.min = min
        self.max = max

    def value_to_string(self, value):
        return str(value)

    def string_to_value(self, string):
        try:
            f = float(string)
            if f > self.max: return self.max
            if f < self.min: return self.min
            return f
        except ValueError:
            return 0.0
