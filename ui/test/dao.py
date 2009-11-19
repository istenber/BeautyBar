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

class TestWithRefDAO(DAO):
    name = db.StringProperty()
    test_ref = db.ReferenceProperty(TestDAO)


def test_dao():
    out = ""
    t = Test("name", "value")
    TestDAO.save(t)
    out += "dbkey = " + str(t.__dbkey__) + "\n"
    lt = TestDAO.load(name="name")
    out += "loaded: " + lt.name + ":" + lt.value + "\n"
    tr = TestWithRef()
    tr.test = t
    TestWithRefDAO.save(tr)
    out += "dbkey = " + str(tr.__dbkey__) + "\n"
    ltr = TestWithRefDAO.load(name="some")
    out += "loaded: " + ltr.name + " with ref " + str(ltr.test) + "\n"
    out += "   " + ltr.test.name + ":" + ltr.test.value + "\n"
    return out


class TestDao(webapp.RequestHandler):
            
    def get(self):        
        self.response.headers['Content-Type'] = "text/plain"
        self.response.out.write(test_dao())
