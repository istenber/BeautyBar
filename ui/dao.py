import logging

from google.appengine.ext import db
from model.data import Item, Data

default_generator="bars"

class GeneratorDAO(db.Model):
    session   = db.StringProperty(required=True)
    generator = db.StringProperty(required=True)

    @staticmethod
    def save(session, generator):
        dao = GeneratorDAO.load_obj(session)
        if dao is None:
            # TODO: we have now many names for session number,
            #       name, session, data_ref - fix to one
            dao = GeneratorDAO(session = session)
        dao.generator = generator
        dao.put()

    @staticmethod
    def load_obj(session):
        return db.GqlQuery("SELECT * FROM GeneratorDAO WHERE session = :1",
                           session).get()

    @staticmethod
    def load(session):
        dao = GeneratorDAO.load_obj(session)
        if dao is not None:
            return dao.generator
        else: return default_generator

class ItemDAO(db.Model):
    name     = db.StringProperty(required=True)
    value    = db.StringProperty(required=True)
    data_ref = db.StringProperty(required=True)
    row      = db.StringProperty(required=True)

    @staticmethod
    def save(ref, c, item):
        dao = db.GqlQuery("SELECT * FROM ItemDAO WHERE" +
                          " row = :1 AND data_ref = :2", 
                          str(c), str(ref)).get()
        if dao is None:
            dao = ItemDAO(name = item.name,
                          data_ref = str(ref))
        dao.value = str(item.value)        
        dao.row = str(c)
        dao.put()

class DataDAO(db.Model):
    name       = db.StringProperty(required=True)
    title      = db.StringProperty(required=True) # TODO: reserved for future
    # TODO: use integers?
    min       = db.StringProperty(required=True)
    max       = db.StringProperty(required=True)

    @staticmethod
    def load(name):
        data = Data()
        items = db.GqlQuery("SELECT * FROM ItemDAO WHERE data_ref = :1 " +
                            "ORDER BY row", name)
        for item in items:
            # TODO: how about row number?!
            data.add_item(Item(item.name, item.value))
        o = db.GqlQuery("SELECT * FROM DataDAO WHERE name = :1", name).get()
        data.set_min(int(o.min))
        data.set_max(int(o.max))
        return data
    
    @staticmethod
    def save(data, name):
        dao = db.GqlQuery("SELECT * FROM DataDAO WHERE name = :1",
                        name).get()
        if dao is None:
            dao = DataDAO(name = str(name))
        dao.title = "no title"
        dao.min = str(data.min)
        dao.max = str(data.max)
        dao.put()
        for c in range(0, len(data.items)):
            ItemDAO.save(name, c, data.items[c])
