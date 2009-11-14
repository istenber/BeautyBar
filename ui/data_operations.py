import random
import logging

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from model.data import Item, Data
from ui.dao import ItemDAO, DataDAO, GeneratorDAO

def make_clean_session():
    session = str(random.randint(1, 10000000))
    data = Data.default()
    DataDAO.save(data, session)
    GeneratorDAO.save(session, "bars")
    return session

class SaveData(webapp.RequestHandler):
    def post(self):
        id = self.request.get("f_savefile")
        if self.request.cookies.has_key("session"):            
            session = str(self.request.cookies["session"])
            data = DataDAO.load(session)
        DataDAO.save(data, id)
        self.redirect("/")

class LoadData(webapp.RequestHandler):
    def post(self):
        id = self.request.get("f_loadfile")
        if self.request.cookies.has_key("session"):            
            session = str(self.request.cookies["session"])
            data = DataDAO.load(id)
        DataDAO.save(data, session)
        self.redirect("/")

class ImportData(webapp.RequestHandler):
    def post(self):
        logging.info("import data")
        file = self.request.get("f_file")
        self.data = Data()
        self._parse_csv(file, self._append_data)

        if self.request.cookies.has_key("session"):            
            session = str(self.request.cookies["session"])
        DataDAO.save(self.data, session)
        
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
        self.response.headers['Set-Cookie'] = "session=" + session
        self.redirect("/")
