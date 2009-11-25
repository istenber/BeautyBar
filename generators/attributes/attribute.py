# TODO: read from dir?
acceptable_types = ["Color", "Choice"]


class Attribute(object):

    def __init__(self, x_name, name, setter, getter):
        self._x_name = x_name
        self._name = name
        self.s = setter
        self.g = getter

    def set(self, val):
        self.s(val)

    def get(self):
        return self.g()

    def name(self):
        return self._name

    def x_name(self):
        return self._x_name

    def type(self):
        return self.__class__.__name__


def is_valid_attribute(attribute):
    # TODO: make have_required_fields and is_derived_from_generator_class
    #       more general and use them here
    if attribute.type() not in acceptable_types:
        print ("# attribute \"" + attribute.name() + "\" " +
               "have incorrect type \"" + attribute.type() + "\"")
        return False
    return True
    
