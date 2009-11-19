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
    def _get_lists(self, dao, obj):
        out = {}
        for list_name in dao.lists():
            if hasattr(obj, list_name):
                l = getattr(obj, list_name)
                out[list_name] = l
            else:
                logging.info("# missing list \"" + list_name + "\"")
        return out

    # @classmethod
    def _save_lists(self, lists):
        for l in lists.iterkeys():
            logging.info("# saving list \"" + l + "\"")
            for obj in lists[l]:
                ref = "__" + self.__class__.__name__[:-3].lower() + "_ref__"
                setattr(obj, ref, self.key())
                DAO.save(obj)

    @classmethod
    def _get_ref_key(self, dao, obj, prop):
        ref_str = "__" + prop + "__"
        if hasattr(obj, ref_str):
            return getattr(obj, ref_str)
        obj_prop = prop[:-4]
        if hasattr(obj, obj_prop):
            obj_ref = getattr(obj, obj_prop)
            # TODO: check missing __dbkey__, means that object is not
            #       stored yet. do we need to store object anyway
            if hasattr(obj_ref, "__dbkey__"):
                return obj_ref.__dbkey__
            else:
                # TODO:
                logging.info("# __dbkey__ missing")
                return None
        logging.info("# prop_ref \"" + obj_prop + "\" and \"" +
                     ref_str + "\" missing!")
        return None

    @classmethod
    def _obj_to_dao(self, obj):
        dao = self._get_dao(obj)
        for prop in dao.properties():
            if prop.endswith("_ref"):
                ref_key = self._get_ref_key(dao, obj, prop)
                if ref_key is None:
                    logging.info("# reference key not found " + prop)
                setattr(dao, prop, ref_key)
                continue
            if hasattr(obj, prop):
                setattr(dao, prop, getattr(obj, prop))
                continue
            logging.info("# prop \"" + prop + "\" not saved")
        return dao

    @classmethod
    def save(self, obj):
        logging.info("# saving " + str(obj))
        dao = self._obj_to_dao(obj)
        dao.put()
        if hasattr(dao, "lists"):
            lists = self._get_lists(dao, obj)
            dao._save_lists(lists)
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
    def load(self, name, dao=""):
        # TODO: if class is not derived use dao as class name
        #         error check one is ok
        logging.info("# loading " + str(name))
        dao = self.gql("WHERE name = :1", name).get()
        if dao is None: return None
        return self._dao_to_obj(dao)


class DataDAO(DAO):
    name = db.StringProperty()
    locked = db.StringProperty()
    min = db.StringProperty()
    max = db.StringProperty()

    def lists(self):
        return ["items"]

class StyleDAO(DAO):
    name = db.StringProperty()
    locked = db.StringProperty()
    # TODO: we cannot use name GeneratorDAO, as it is not defined yet,
    #       and we cannot define it before StyleDAO as there is dependency
    #       there. So just use unnamed reference
    generator_ref = db.ReferenceProperty()

class GeneratorDAO(DAO):
    name = db.StringProperty()
    style_ref = db.ReferenceProperty(StyleDAO)

class OutputDAO(DAO):
    name = db.StringProperty()
    # TODO: fix to db diagram
    content_type = db.StringProperty()
    content = db.StringProperty()
    data_ref = db.ReferenceProperty(DataDAO)
    style_ref = db.ReferenceProperty(StyleDAO)

class SessionDAO(DAO):
    name = db.StringProperty()
    data_ref = db.ReferenceProperty(DataDAO)
    style_ref = db.ReferenceProperty(StyleDAO)
    output_ref = db.ReferenceProperty(OutputDAO)

class AttributeDAO(DAO):
    name = db.StringProperty()
    value = db.StringProperty()
    generator_ref = db.ReferenceProperty(GeneratorDAO)

class ItemDAO(DAO):
    name = db.StringProperty()
    value = db.StringProperty()
    row = db.StringProperty()
    data_ref = db.ReferenceProperty(DataDAO)

class Item(object):
    def __init__(self, name="", value="", row=""):
        self.name = name
        self.value = value
        self.row = row
        # self.data = None # TODO: data_ref

class Data(object):
    def __init__(self, name="", min="", max=""):
        self.name = name
        self.locked = "false" # TODO: fix to boolean
        self.min = min
        self.max = max
        self.items = []

class Output(object):
    def __init__(self, name=""):
        self.name = name
        self.content_type = "text/plain"
        self.content = None
        self.data = None # TODO: data_ref
        self.style = None # TODO: style_ref

class Session(object):
    def __init__(self, name=""):
        self.name = name
        self.data = None # TODO: data_ref
        self.style = None # TODO: style_ref
        self.output = None # TODO: output_ref

class Style(object):
    def __init__(self, name=""):
        self.name = name
        self.locked = "false" # TODO: fix to boolean
        self.generator = None # TODO: generator_ref

class Generator(object):
    def __init__(self, name=""):
        self.name = name
        self.style = None # TODO: style_ref

class Attribute(object):
    def __init__(self, name="", value=""):
        self.name = name
        self.value = value
        self.generator = None # TODO: generator_ref

