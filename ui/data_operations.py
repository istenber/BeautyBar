import random
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

class CleanData(webapp.RequestHandler):
    def get(self):
        self._clean()
    def post(self):
        self._clean()        
    def _clean(self):
        session = make_clean_session()
        self.response.headers['Set-Cookie'] = "session=" + session
        self.redirect("/")
