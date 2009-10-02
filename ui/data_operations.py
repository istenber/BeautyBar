import random
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

class CleanData(webapp.RequestHandler):
    def get(self):
        self._clean()
    def post(self):
        self._clean()        
    def _clean(self):
        session = str(random.randint(1, 10000000))
        self.response.headers['Set-Cookie'] = "session=" + session
        self.redirect("/")
