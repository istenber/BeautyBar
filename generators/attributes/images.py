from attribute import Attribute


class Imagechoice(Attribute):

    def __init__(self, generator, name, ui_name, choices):
        Attribute.__init__(self, generator, name, ui_name)
        self.choices = choices

    def value_to_string(self, value):
        return str(value)

    def string_to_value(self, string):
        return int(string)
