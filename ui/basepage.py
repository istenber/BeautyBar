import os
import random
import logging

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from ui.data_operations import make_clean_session
from ui.dao import DAO

class Page(webapp.RequestHandler):

    def __init__(self):
        webapp.RequestHandler.__init__(self)
        self.values = {}

    def get_values(self):
        """Override me!"""

    def get(self):
        self.values.update(self.get_values())
        if not 'debug' in self.values:
            self.values['debug'] = "(none)"
        if 'template' in self.values:
            self.values['template'] += ".html"
        else:
            self.values['template'] = self.__class__.__name__.lower() + ".html"
        path = os.path.join(os.path.dirname(__file__),
                            '../templates/base.html')
        self.response.out.write(template.render(path, self.values))


class ExtraPage(Page):
    pass


class ActivePage(Page):

    def get(self):
        self.get_session()
        self.values['use_javascript'] = True
        Page.get(self)

    def get_session(self):
        if self.request.cookies.has_key("session"):            
            session_name = str(self.request.cookies["session"])
            self.session = DAO.load(name=session_name, class_name="Session")
            if not self.session:
                self.session = make_clean_session(self.request.remote_addr)
        else:
            self.session = make_clean_session(self.request_remote_addr)
        self.response.headers['Set-Cookie'] = "session=" + self.session.name
