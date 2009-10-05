import random
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from model.data import Item, Data
from ui.dao import ItemDAO, DataDAO

class CleanData(webapp.RequestHandler):
    def get(self):
        self._clean()
    def post(self):
        self._clean()        
    def _clean(self):
        session = str(random.randint(1, 10000000))
        data = Data.default()
        DataDAO.save(data, session)
        self.response.headers['Set-Cookie'] = "session=" + session
        self.redirect("/")
