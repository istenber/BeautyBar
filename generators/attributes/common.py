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


class Random(Attribute):

    def value_to_string(self, value):
        return str(value)

    def string_to_value(self, string):
        return int(string)


class Float(Attribute):

    def __init__(self, generator, name, ui_name, min, max):
        Attribute.__init__(self, generator, name, ui_name)
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


class Integer(Attribute):

    def __init__(self, generator, name, ui_name, min, max, default):
        Attribute.__init__(self, generator, name, ui_name)
        self.min = min
        self.max = max
        self.default = default

    def value_to_string(self, value):
        return str(value)

    def string_to_value(self, string):
        try:
            i = int(string)
            if i > self.max: return self.max
            if i < self.min: return self.min
            return i
        except ValueError:
            return 0.0


class Title(Attribute):

    def __init__(self, generator, ui_name):
        Attribute.__init__(self, generator, 'title', ui_name)

    def get_ui_name(self):
        return '<b>' + Attribute.get_ui_name(self) + '</b>'

    def get_value(self):
        return ''

    def set_value(self, value):
        pass

    def value_to_string(self, value):
        return ''

    def string_to_value(self, string):
        return ''
