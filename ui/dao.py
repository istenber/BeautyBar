import logging

from google.appengine.ext import db
import model

__all__ = ['Item', 'Data', 'Output', 'Session',
           'Generator', 'Attribute', 'Style']

class Dao(db.Model):

    # TODO: check list properties and generate methods:
    #   get_<list_name>
    #   add_<list_name in singular>

    # TODO: optimize list loading... don't load list if it already exists

    def add_to_list(self, list, item):
        if not item.is_saved():
            item.put()
        list.append(item.key())

    @classmethod
    def objfac(cls, new_cls, **kwds):
        return eval(new_cls)(**kwds)

    def __setattr__(self, attr, value):
        if isinstance(value, Dao) and not value.is_saved():
            value.put()
        db.Model.__setattr__(self, attr, value)

    # TODO: does NOT work with elems with loops
    # TODO: generators and active generator should be same!!!
    # blacklist = { old_key_1: new_key_1, old_key_2: new_key_2, ... }
    def copy_model_instance(self, blacklist=dict(), instance=None):
        # logging.info("# " + str(blacklist) + ":::" + str(instance))
        initial = dict()
        for name in self.properties():
            value = getattr(self, name)
            if isinstance(value, db.Model):
                if str(value.key()) in blacklist:
                    value = Dao.get(blacklist[str(value.key())])
                else:
                    newone = value.__class__()
                    newone.put()
                    blacklist[str(value.key())] = str(newone.key())
                    value = value.copy_model_instance(blacklist, newone)
                    value.put()
            if isinstance(value, list):
                # TODO: this is only for keylists, there might be
                #       other kind of lists as well
                l = []
                for key in value:
                    if str(key) in blacklist:
                        l.append(Dao.get(blacklist[str(key)]))
                    else:
                        elem = Dao.get(key)
                        newone = elem.__class__()
                        newone.put()
                        blacklist[str(key)] = str(newone.key())
                        elem = elem.copy_model_instance(blacklist, newone)
                        elem.put()
                        l.append(elem.key())
                value = l
            initial[name] = value
        if instance is None:
            return self.__class__(**initial)
        else:
            # updating dict does not work, as django/app engine
            # uses special variables for properties
            for prop in initial:
                setattr(instance, prop, initial[prop])
            return instance


class Data(Dao, model.data.Data):
    name = db.StringProperty()
    locked = db.BooleanProperty()
    min = db.FloatProperty()
    max = db.FloatProperty()
    items = db.ListProperty(db.Key) # Item

    def get_items(self):
        return Item.get(self.items)

    def _add_item(self, item):
        return self.add_to_list(self.items, item)


class Style(Dao, model.style.Style):
    name = db.StringProperty()
    locked = db.BooleanProperty()
    generators = db.ListProperty(db.Key) # Generator
    active_generator = db.ReferenceProperty() # Generator

    def get_generators(self):
        return Generator.get(self.generators)

    def add_generator(self, generator):
        return self.add_to_list(self.generators, generator)


class Generator(Dao, model.generator.Generator):
    name = db.StringProperty()
    # TODO: is needed?
    # style = db.ReferenceProperty(Style)
    attributes = db.ListProperty(db.Key) # Attribute

    def get_attributes(self):
        return Attribute.get(self.attributes)

    def add_attribute(self, attribute):
        return self.add_to_list(self.attributes, attribute)


class Output(Dao, model.output.Output):
    name = db.StringProperty()
    content_type = db.StringProperty()
    content = db.StringProperty()
    # TODO: backward reference? maybe not needed?
    data = db.ReferenceProperty(Data)
    style = db.ReferenceProperty(Style)


class Session(Dao, model.session.Session):
    name = db.StringProperty()
    cookie = db.StringProperty()
    ip_address = db.StringProperty()
    data = db.ReferenceProperty(Data)
    style = db.ReferenceProperty(Style)
    # TODO: is needed?
    # output = db.ReferenceProperty(Output)

    @classmethod
    def load(cls, cookie):
        session = cls.gql("WHERE cookie = :1", cookie).get()
        if session is None:
            logging.info("Session missing (" + cookie + ")")
        return session

    @classmethod
    def load_file(cls, filename):
        return cls.gql("WHERE name = :1", filename).get()


class Attribute(Dao, model.generator.Attribute):
    name = db.StringProperty()
    value = db.StringProperty()


class Item(Dao, model.data.Item):
    name = db.StringProperty()
    value = db.FloatProperty()
    row = db.IntegerProperty()

# TODO: remove attribute generator ref and item data ref from db model image
