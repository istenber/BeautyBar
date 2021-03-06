import random
import logging

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from ui.basepage import SessionPage
from google.appengine.api import users
import lib.string_utils
import ui.dao


DEFAULT_STYLES = ['gradient', 'nature', 'plain', 'towers', 'bottombar']


class Dataset(SessionPage):

    def get(self):
        self.get_session()
        name = self.request.get("name")
        if name == "":
            return
        if not name in ['google', 'clean', 'simple']:
            return
        for item in self.session.data.get_items():
            item.delete()
        self.session.data.delete()
        self.session.data = eval('ui.dao.Data.default_' + name)()
        self.session.put()


class SaveData(SessionPage):

    def get(self):
        self.get_session()
        filename = lib.string_utils.unquote(self.request.get("name"))
        if not filename.find("@") == -1:
            self.response.out.write("@ is reserved char")
            return
        if (filename in DEFAULT_STYLES) and (not users.is_current_user_admin()):
            self.response.out.write("%s is reserved name" % filename)
            return
        old_file = ui.dao.Session.load_file(filename)
        if old_file is None:
            self.response.out.write("Saved as " + filename)
            version = 1
        else:
            old_name = filename + "@" + str(old_file.version)
            old_file.name = old_name
            old_file.put()
            self.response.out.write(filename + " replaced " +
                                    "<small>(old is " + old_name + ")</small>")
            # we need this as there are old files without version number
            if old_file.version is not None:
                version = old_file.version + 1
            else:
                version = 2
        newone = self.session.copy_model_instance()
        newone.name = filename
        newone.cookie = ""
        newone.version = version
        newone.put()


class LoadData(SessionPage):

    def get(self):
        self.get_session()
        filename = lib.string_utils.unquote(self.request.get("name"))
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
        if self.request.get("redirect") == "yes":
            self.redirect("/")
            return
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
