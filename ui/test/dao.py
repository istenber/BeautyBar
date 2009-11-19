import logging

from google.appengine.ext import db
from google.appengine.ext import webapp

from ui.dao import DAO
# TODO: move to model.<name>
from ui.dao import Output, Session, Style, Generator, Attribute
from ui.dao import SessionDAO
from model.data import Data, Item

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


def test_query():
    out = ""
    from google.appengine.ext.db import GqlQuery
    from google.appengine.ext import db
    session_name = "test-session-123"
    q = GqlQuery("SELECT * FROM SessionDAO WHERE name = :1", session_name)
    out += "count: " + str(q.count()) + "\n"
    o = q.get()
    out += "obj: " + str(o) + "\n"
    out += "  " + str(o.key()) + "\n"
    s = SessionDAO.load(name=session_name)
    out += "ses: " + str(s) + "\n"
    out += "  " + str(s.__dbkey__) + "\n"
    return out


def make_data():
    d = Data(name="ds")
    for c in range(0, 3):
        name = "n" + str(c)
        i = Item(name=name, value=c*2, row=c)
        d.items.append(i)
    return d

def make_style():
    s = Style(name="cust-style")
    g = Generator(name="gengen")
    a = Attribute(name="color", value="red")
    g.attributes.append(a)
    a = Attribute(name="bgcolor", value="blue")
    g.attributes.append(a)
    s.generators.append(g)
    g.active = "true"
    return s

def make_output(d, s):
    o = Output(name="outti")
    o.content = "hello world"
    o.data = d
    o.style = s
    return o

def test_daos():
    out = ""
    ses = Session("test-session-123")
    out += "session: " + ses.name + "\n"
    d = make_data()
    out += "data: " + d.name + "\n"
    for i in d.items:
        out += "   + " + i.name + "\n"
    DAO.save(d)
    s = make_style()
    out += "style: " + s.name + "\n"
    o = make_output(d, s)
    out += "output: " + o.name + "\n"
    ses.data = d
    ses.style = s
    ses.output = o
    DAO.save(ses)
    out += "a : " + str(ses.__dbkey__) + "\n"
    ls = DAO.load(name="test-session-123", class_name="Session")
    out += "\n\n------------- loading --------------\n\n"
    out += "b : " + str(ls.__dbkey__) + "\n"
    out += "data: " + ls.data.name + "\n"
    for i in ls.data.items:
        out += "   + " + i.name + "\n"
    out += "style: " + ls.style.name + "\n"
    out += "output: " + ls.output.name + "\n"
    return out

class TestDao(webapp.RequestHandler):
            
    def get(self):        
        self.response.headers['Content-Type'] = "text/plain"

        self.response.out.write("\ntest_query()\n")
        self.response.out.write("--------------------------\n")
        self.response.out.write(test_query())

        self.response.out.write("\ntest_base_dao()\n")
        self.response.out.write("--------------------------\n")
        self.response.out.write(test_base_dao())

        self.response.out.write("\ntest_daos() \n")
        self.response.out.write("--------------------------\n")
        self.response.out.write(test_daos())
