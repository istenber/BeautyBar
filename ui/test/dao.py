import logging

from google.appengine.ext import db
from google.appengine.ext import webapp

from ui.dao import DAO

# test_dao # TestDAO, Test, TrDAO, Tr

# --------------- test program -------------------

class Test(object):
    def __init__(self, name="", value=""):
        self.name = name
        self.value = value

class TestWithRef(object):
    def __init__(self):
        self.name = "some"
        self.test = None


class TestDAO(DAO):
    value = db.StringProperty()
    name = db.StringProperty()

    def get_object_module(self):
        return "ui.test.dao"

class TestWithRefDAO(DAO):
    name = db.StringProperty()
    test_ref = db.ReferenceProperty(TestDAO)

def test_base_dao():
    out = ""
    t = Test("name", "value")
    # TestDAO.save(t)
    DAO.save(t)
    out += "dbkey = " + str(t.__dbkey__) + "\n"
    lt = TestDAO.load(name="name")
    out += "loaded: " + lt.name + ":" + lt.value + "\n"
    tr = TestWithRef()
    tr.test = t
    # TestWithRefDAO.save(tr)
    DAO.save(tr)
    out += "dbkey = " + str(tr.__dbkey__) + "\n"
    ltr = TestWithRefDAO.load(name="some")
    out += "loaded: " + ltr.name + " with ref " + str(ltr.test) + "\n"
    out += "   " + ltr.test.name + ":" + ltr.test.value + "\n"
    return out

def test_daos():
    out = ""
    from ui.dao import Item, ItemDAO
    from ui.dao import Data, DataDAO
    from ui.dao import Output, OutputDAO
    from ui.dao import Session, SessionDAO
    from ui.dao import Style, StyleDAO
    from ui.dao import Generator, GeneratorDAO
    from ui.dao import Attribute, AttributeDAO
    i1 = Item()
    # DAO.save(i1)
    out += "i1: " + str(i1) + "\n"
    i2 = Item()
    # DAO.save(i2)
    out += "i2: " + str(i2) + "\n"
    d = Data()
    d.items = [i1, i2]
    DAO.save(d)
    out += "d: " + str(d) + "\n"
    out += "i2.__data_ref__: " + str(i2.__data_ref__) + "\n"
    return out

class TestDao(webapp.RequestHandler):
            
    def get(self):        
        self.response.headers['Content-Type'] = "text/plain"

        self.response.out.write("\ntest_base_dao()\n")
        self.response.out.write("--------------------------\n")
        self.response.out.write(test_base_dao())

        self.response.out.write("\ntest_daos() \n")
        self.response.out.write("--------------------------\n")
        self.response.out.write(test_daos())
