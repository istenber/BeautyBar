import logging

from google.appengine.ext import db
from model.data import Item, Data

class GeneratorDAO(db.Model):
    session   = db.StringProperty(required=True)
    generator = db.StringProperty(required=True)

    @staticmethod
    def save(session, generator):
        if GeneratorDAO.load(session) is None:
            GeneratorDAO(session = session,
                         generator = generator).put()
    @staticmethod
    def load(session):
        o = db.GqlQuery("SELECT * FROM GeneratorDAO WHERE session = :1", 
                        session).get()
        if o is not None:
            return o.generator
        else: return None    

class ItemDAO(db.Model):
    name     = db.StringProperty(required=True)
    value    = db.StringProperty(required=True)
    data_ref = db.StringProperty(required=True)
    row      = db.StringProperty(required=True)

    @staticmethod
    def save(ref, c, item):
        old = db.GqlQuery("SELECT * FROM ItemDAO WHERE" +
                          " row = :1 AND data_ref = :2", 
                          str(c), str(ref))
        if not old.count() == 0:
            dao = old[0]
            dao.name = str(item.name)
            dao.value = str(item.value)
        else:
            dao = ItemDAO(name     = str(item.name),
                          value    = str(item.value),
                          data_ref = str(ref),
                          row      = str(c),
                          )
        dao.put()

class DataDAO(db.Model):
    name       = db.StringProperty(required=True)
    
    @staticmethod
    def load(name):
        data = Data()
        items = db.GqlQuery("SELECT * FROM ItemDAO WHERE data_ref = :1 " +
                            "ORDER BY row", name)
        for item in items:
            data.add_item(Item(item.name, item.value))
        return data
    
    @staticmethod
    def save(data, name):
        old = db.GqlQuery("SELECT * FROM DataDAO WHERE name = :1",
                          name)
        if not old.count() == 0:
            dao = old[0]
        else:
            dao = DataDAO(name = str(name))
            dao.put()
        for c in range(0, len(data.items)):
            ItemDAO.save(name, c, data.items[c])
