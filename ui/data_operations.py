import random
import logging

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from model.data import Item, Data
from model.session import Session
from model.output import Output
from model.style import Style
from ui.dao import DAO

def _generate_session_id():
    return str(random.randint(1, 10000000))

def make_clean_session():
    ses = Session(name=_generate_session_id())

    data = Data.default()
    data.locked = "true"

    style = Style.default()
    style.locked = "true"

    output = Output()
    output.data = data
    output.style = style

    ses.data = data
    ses.output = output
    ses.style = style

    DAO.save(ses)
    return ses

# TODO: note saves data AND style
class SaveData(webapp.RequestHandler):
    def post(self):
        new_name = self.request.get("f_savefile")
        if self.request.cookies.has_key("session"):
            name = str(self.request.cookies["session"])
            session = DAO.load(name=name, class_name="Session")
        self.response.headers['Set-Cookie'] = "session=" + new_name
        session.name = new_name
        # TODO: delete old entry?
        DAO.save(session)
        self.redirect("/")

# TODO: note loads data AND style
class LoadData(webapp.RequestHandler):
    def post(self):
        old_name = self.request.get("f_loadfile")
        self.response.headers['Set-Cookie'] = "session=" + old_name
        self.redirect("/")

class ImportData(webapp.RequestHandler):
    def post(self):
        logging.info("import data")
        file = self.request.get("f_file")
        # TODO: if there is no session!!?
        if self.request.cookies.has_key("session"):
            name = str(self.request.cookies["session"])
            session = DAO.load(name=name, class_name="Session")
        self.data = Data()
        self._parse_csv(file, self._append_data)
        session.data = self.data
        DAO.save(session)
        self.redirect("/")

    def _append_data(self, name, value):
        self.data.add_item(Item(name, value))

    def _parse_csv(self, csv, f):
        for line in csv.splitlines():
            if line == "": continue
            try:
                (name, value) = line.split(",")
            except ValueError, e:
                print str(e) + " in \"" + line + "\""
                continue
            name = name.strip()
            value = value.strip()
            f(name, value)

class CleanData(webapp.RequestHandler):
    def get(self):
        self._clean()
    def post(self):
        self._clean()
    def _clean(self):
        session = make_clean_session()
        self.response.headers['Set-Cookie'] = "session=" + session.name
        self.redirect("/")
