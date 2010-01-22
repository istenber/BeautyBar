import logging

from google.appengine.ext import db
from google.appengine.ext.db import NotSavedError
import model

__all__ = ['Item', 'Data', 'Output', 'Session',
           'Generator', 'Attribute', 'Style']

class Dao(db.Model):

    # TODO: check list properties and generate methods:
    #   get_<list_name>
    #   add_<list_name in singular>

    # TODO: optimize list loading... don't load list if it already exists

    # TODO: caching...

    def add_to_list(self, list, item):
        try:
            list.append(item.key())
        except NotSavedError:
            item.put()
            list.append(item.key())

    @classmethod
    def objfac(self, cls, **kwds):
        return eval(cls)(**kwds)


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
    def load(self, cookie):
        session = self.gql("WHERE cookie = :1", cookie).get()
        if session is None:
            logging.info("Session missing (" + cookie + ")")
        return session


class Attribute(Dao, model.generator.Attribute):
    name = db.StringProperty()
    value = db.StringProperty()


class Item(Dao, model.data.Item):
    name = db.StringProperty()
    value = db.FloatProperty()
    row = db.IntegerProperty()

# TODO: remove attribute generator ref and item data ref from db model image
