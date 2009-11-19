import logging

from google.appengine.ext import db
from model.data import Item, Data

default_generator="bars"

class DAO(db.Model):
    # DAOs must be in this file or within same file with objects...

    # TODO: handle lists...
    # TODO: take care of reference loops
    # TODO: support to other properties (not StringProperty)

    @classmethod
    def _get_dao(self, obj):
        dao_class = obj.__class__.__name__ + "DAO"
        try:
            return eval(dao_class)()
        except NameError, er:
            module = obj.__module__
            logging.info("# dao class missing, lets import: " + module)
            import_cmd = "from " + module + " import " + dao_class
            exec(import_cmd)
        try: 
            return eval(dao_class)()
        except NameError, er:
            logging.info("# import didn't help")
            return None

    @classmethod
    def _obj_to_dao(self, obj):
        dao = self._get_dao(obj)
        for prop in dao.properties():
            if prop.endswith("_ref"):
                obj_prop = prop[:-4]
                obj_ref = getattr(obj, obj_prop)
                logging.info("# XXX: references are not saved!")
                # TODO: check missing __dbkey__, means that object is not
                #       stored yet. do we need to store object anyway
                setattr(dao, prop, obj_ref.__dbkey__)
                continue
            if hasattr(obj, prop):
                setattr(dao, prop, getattr(obj, prop))
            else:
                logging.info("# prop \"" + prop + "\" not found")
        return dao

    @classmethod
    def save(self, obj):
        logging.info("# saving " + str(obj))
        dao = self._obj_to_dao(obj)
        dao.put()
        obj.__dbkey__ = dao.key()

    @classmethod
    def _get_obj(self, dao):
        obj_class = self.__name__[:-3]
        try:
            return eval(obj_class)()
        except NameError, er:
            if hasattr(dao, "get_object_module"):
                module = dao.get_object_module()
            else: module = dao.__module__
            logging.info("# obj class missing, lets import: " + module)
            import_cmd = "from " + module + " import " + obj_class
            exec(import_cmd)
        try: 
            return eval(obj_class)()
        except NameError, er:
            logging.info("# import didn't help")
            return None

    @classmethod
    def _dao_to_obj(self, dao):
        obj = self._get_obj(dao)
        for prop in dao.properties():
            if prop.endswith("_ref"):
                obj_prop = prop[:-4]
                ref_dao = getattr(dao, prop)
                ref_obj = ref_dao._dao_to_obj(ref_dao)
                setattr(obj, obj_prop, ref_obj)
                continue
            if hasattr(obj, prop):
                setattr(obj, prop, getattr(dao, prop))
            else:
                logging.info("# prop \"" + prop + "\" not found")        
        return obj

    @classmethod
    def load(self, name):
        logging.info("# loading " + str(name))
        dao = self.gql("WHERE name = :1", name).get()
        if dao is None: return None
        return self._dao_to_obj(dao)

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

