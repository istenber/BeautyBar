import logging

from google.appengine.ext import db
from model.data import Item, Data

default_generator="bars"

# TODO: refactor to use base class!!!

class GenParamsDAO(db.Model):
    session = db.StringProperty()   # TODO: lets use real foreign key
    generator = db.StringProperty() #         session+generator
    content = db.StringProperty()

    @staticmethod
    def save(session, gen):
        dao = GenParamsDAO.load_obj(session, gen)
        if dao is None:
            dao = GeneratorDAO()
        dao.session = session
        dao.generator = gen
        # TODO: GeneratorFAc...generator.export_attributes()
        dao.content = "no params"
        dao.put()

    @staticmethod
    def load_obj(session, gen):
        return db.GqlQuery("SELECT * FROM GenParamsDAO WHERE " + 
                           "session = :1 AND generator = :2",
                           session, gen).get()

    @staticmethod
    def load(session, gen):
        dao = GenParamsDAO.load_obj(session, gen)
        if dao is not None:
            # TODO: GeneratorFAc... <-- g, g.import_attributes()
            return dao.generator
        else: return default_generator

class GeneratorDAO(db.Model):
    session   = db.StringProperty()
    generator = db.StringProperty()

    @staticmethod
    def save(session, generator):
        dao = GeneratorDAO.load_obj(session)
        if dao is None:
            # TODO: we have now many names for session number,
            #       name, session, data_ref - fix to one
            dao = GeneratorDAO()
        dao.session = session
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
    name     = db.StringProperty()
    value    = db.StringProperty()
    data_ref = db.StringProperty()
    row      = db.StringProperty()

    @staticmethod
    def save(ref, c, item):
        dao = db.GqlQuery("SELECT * FROM ItemDAO WHERE" +
                          " row = :1 AND data_ref = :2", 
                          str(c), str(ref)).get()
        if dao is None:
            dao = ItemDAO()
        dao.name = item.name
        dao.data_ref = str(ref)
        dao.value = str(item.value)        
        dao.row = str(c)
        dao.put()

class DataDAO(db.Model):
    name       = db.StringProperty()
    title      = db.StringProperty() # TODO: reserved for future
    # TODO: use integers?
    min       = db.StringProperty()
    max       = db.StringProperty()

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
            dao = DataDAO()
        dao.name = str(name)
        dao.title = "no title"
        dao.min = str(data.min)
        dao.max = str(data.max)
        dao.put()
        for c in range(0, len(data.items)):
            ItemDAO.save(name, c, data.items[c])
