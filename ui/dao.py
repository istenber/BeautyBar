import logging

from google.appengine.ext.db import GqlQuery
from google.appengine.ext import db
from model.data import Item, Data


default_generator = "bars"
max_query_items = 100


class DAO(db.Model):
    # DAOs must be in this file or within same file with objects...

    # TODO: handle lists...
    # TODO: take care of reference loops
    # TODO: support to other properties (not StringProperty)
    # TODO: only single ReferenceProperty for each class type allowed
    # TODO: implement blacklist as cross reference check

    @classmethod
    def _new_or_load(self, dao_class, obj, import_cmd=None):
        # TODO: catch import error!?
        if import_cmd: exec(import_cmd)
        if hasattr(obj, "__dbkey__"):
            return eval(dao_class).get(obj.__dbkey__)
        else:
            return eval(dao_class)()

    @classmethod
    def _get_dao(self, obj):
        dao_class = obj.__class__.__name__ + "DAO"
        try:
            return self._new_or_load(dao_class, obj)
        except NameError, er:
            module = obj.__module__
            # logging.info("# \"" + dao_class + "\" class missing, " +
            #              "lets import it from \"" + module + "\"")
        import_cmd = "from " + module + " import " + dao_class
        try: 
            return self._new_or_load(dao_class, obj, import_cmd)
        except NameError, er:
            logging.info("# import failed for dao_class " + dao_class)
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
            # logging.info("# saving list \"" + l + "\"")
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
            if not hasattr(obj_ref, "__dbkey__"):
                # logging.info("# saving referenced object " + str(obj_ref))
                DAO.save(obj_ref)
            return obj_ref.__dbkey__
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
        # logging.info("# saving " + str(obj))
        dao = self._obj_to_dao(obj)
        dao.put()
        lists = self._get_lists(dao, obj)
        dao._save_lists(lists)
        obj.__dbkey__ = dao.key()

    @classmethod
    def _get_obj(self, dao):
        obj_class = dao.__class__.__name__[:-3]
        try:
            return eval(obj_class)()
        except NameError, er:
            if hasattr(dao, "get_object_module"):
                module = dao.get_object_module()
            else: module = dao.__module__
            # logging.info("# eval failed, lets import \"" +
            #              obj_class + "\" from \"" + module + "\"")
        import_cmd = "from " + module + " import " + obj_class
        exec(import_cmd)
        try: 
            return eval(obj_class)()
        except NameError, er:
            logging.info("# import failed for obj_class " + obj_class)
            return None

    @classmethod
    def _get_old_ref(self, refs, prop):
        for ref in refs:
            if ref[0] == prop: return ref[1]
        return None

    @classmethod
    def _get_ref_obj(self, dao, prop, refs):
        old_ref = self._get_old_ref(refs, prop)
        if old_ref: return old_ref
        ref_dao = getattr(dao, prop)
        return ref_dao._dao_to_obj(ref_dao, refs)

    @classmethod
    def _load_lists(self, dao, obj, refs):
        my_ref = dao.__class__.__name__[:-3].lower() + "_ref"
        my_val = dao.key()
        refs.append([my_ref, obj])
        for list_name in dao.lists():
            # logging.info("# loading list \"" + list_name + "\"")
            list_class = list_name[:-1].capitalize() + "DAO"
            q = eval(list_class).gql("WHERE " + my_ref + " = :1", my_val)
            l = []
            for list_dao in q.fetch(max_query_items):
                l_obj = list_dao._dao_to_obj(list_dao, refs)
                setattr(l_obj, "__" + my_ref + "__", obj) # TODO: dao or obj?
                l.append(l_obj)
            setattr(obj, list_name, l)

    @classmethod
    def _dao_to_obj(self, dao, refs):
        # logging.info("# _dao_to_obj: loading " + str(dao))
        obj = self._get_obj(dao)
        for prop in dao.properties():
            if prop.endswith("_ref"):
                ref_obj = self._get_ref_obj(dao, prop, refs)
                obj_prop = prop[:-4]
                setattr(obj, obj_prop, ref_obj)
                continue
            if hasattr(obj, prop):
                setattr(obj, prop, getattr(dao, prop))
            else:
                # TODO: this can be sometimes ok as well, as we have
                #       make list reference!
                logging.info("# prop \"" + prop + "\" not found")
        self._load_lists(dao, obj, refs)
        obj.__dbkey__ = dao.key()
        return obj

    @classmethod
    def load(self, name, class_name=None):
        # logging.info("# loading " + str(name))
        if class_name:
            dao_class = class_name + "DAO"
            dao = GqlQuery("SELECT * FROM " + dao_class +
                           " WHERE name = :1", name).get()
        else:
            dao = self.gql("WHERE name = :1", name).get()
        if dao is None:
            logging.info("# object not found from db")
            return None
        obj = dao._dao_to_obj(dao, [])
        return obj

    def lists(self):
        """ Override me with name of lists in class. """
        return []


class DataDAO(DAO):
    name = db.StringProperty()
    locked = db.BooleanProperty()
    min = db.IntegerProperty()
    max = db.IntegerProperty()

    def lists(self):
        return ["items"]

    def get_object_module(self):
        return "model.data"


class StyleDAO(DAO):
    name = db.StringProperty()
    locked = db.BooleanProperty()

    def lists(self):
        return ["generators"]

    def get_object_module(self):
        return "model.style"


class GeneratorDAO(DAO):
    name = db.StringProperty()
    active = db.BooleanProperty()
    style_ref = db.ReferenceProperty(StyleDAO)

    def lists(self):
        return ["attributes"]

    def get_object_module(self):
        return "model.generator"


class OutputDAO(DAO):
    name = db.StringProperty()
    content_type = db.StringProperty()
    content = db.StringProperty()
    data_ref = db.ReferenceProperty(DataDAO)
    style_ref = db.ReferenceProperty(StyleDAO)

    def get_object_module(self):
        return "model.output"


class SessionDAO(DAO):
    name = db.StringProperty()
    data_ref = db.ReferenceProperty(DataDAO)
    style_ref = db.ReferenceProperty(StyleDAO)
    output_ref = db.ReferenceProperty(OutputDAO)

    def get_object_module(self):
        return "model.session"


class AttributeDAO(DAO):
    name = db.StringProperty()
    value = db.StringProperty()
    generator_ref = db.ReferenceProperty(GeneratorDAO)

    def get_object_module(self):
        return "model.generator"


class ItemDAO(DAO):
    name = db.StringProperty()
    value = db.IntegerProperty()
    row = db.IntegerProperty()
    data_ref = db.ReferenceProperty(DataDAO)

    def get_object_module(self):
        return "model.data"
