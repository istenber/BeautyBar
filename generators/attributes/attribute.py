# TODO: read from dir?
acceptable_types = ["Color", "Boolean"]


class Attribute(object):

    def __init__(self, generator, name, ui_name):
        self.generator = generator
        self.name = name
        self.ui_name = ui_name

    def get_name(self):
        return self.name

    def get_ui_name(self):
        return self.ui_name

    def get_type(self):
        return self.__class__.__name__

    def get_value(self):
        return self.value_to_string(getattr(self.generator, self.name))

    def set_value(self, value):
        return setattr(self.generator, self.name, self.string_to_value(value))

    def value_to_string(self, value):
        return value

    def string_to_value(self, string):
        return string


def is_valid_attribute(attribute):
    # TODO: make have_required_fields and is_derived_from_generator_class
    #       more general and use them here
    if attribute.get_type() not in acceptable_types:
        print ("# attribute \"" + attribute.get_name() + "\" " +
               "have incorrect type \"" + attribute.get_type() + "\"")
        return False
    return True
    
