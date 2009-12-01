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
