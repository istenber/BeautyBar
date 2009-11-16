acceptable_types = ["Color", "Choice"]

class Attribute(object):
    def name(self):
        pass
    def type(self):
        pass

def is_valid_attribute(attribute):
    # TODO: make have_required_fields and is_derived_from_generator_class
    #       more general and use them here
    if attribute.type() not in acceptable_types:
        print ("# attribute \"" + attribute.name() + "\" " +
               "have incorrect type \"" + attribute.type() + "\"")
        return False
    return True
    
