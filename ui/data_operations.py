import random
import logging

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from ui.basepage import SessionPage
import ui.dao


class SaveData(SessionPage):

    def get(self):
        self.get_session()
        filename = self.request.get("name")
        old_file = ui.dao.Session.load_file(filename)
        if old_file is None:
            self.response.out.write("Saved as " + filename)
        else:
            self.session.name = "_deleted"
            self.session.put()
            self.response.out.write("Replaced old " + filename)
        newone = self.session.copy_model_instance()
        newone.name = filename
        newone.cookie = ""
        newone.put()


class LoadData(SessionPage):

    def get(self):
        self.get_session()
        filename = self.request.get("name")
        old_file = ui.dao.Session.load_file(filename)
        if old_file is None:
            self.response.out.write("Cannot find " + filename)
            return
        newone = old_file.copy_model_instance()
        newone.name = ""
        newone.cookie = self.session.cookie
        newone.put()
        self.session.name = "_deleted"
        self.session.cookie = ""
        self.session.put()
        self.response.out.write(filename + " loaded")


class ImportData(SessionPage):

    def post(self):
        self.get_session()
        filename = self.request.get("f_file")
        d = ui.dao.Data.parse_csv(filename)
        if d is not None:
            d.put()
            self.session.data = d
            self.session.put()
        self.redirect("/")


class CleanData(webapp.RequestHandler):
    def get(self):
        self._clean()
    def post(self):
        self._clean()
    def _clean(self):
        session = ui.dao.Session.default(self.request.remote_addr)
        session.put()
        self.response.headers['Set-Cookie'] = "session=" + session.cookie
        self.redirect("/")
