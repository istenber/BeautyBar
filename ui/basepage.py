import os
import random
import logging

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.api import users
import ui.dao

class Page(webapp.RequestHandler):

    def __init__(self):
        webapp.RequestHandler.__init__(self)
        self.values = {}

    def get_values(self):
        """Override me!"""

    def is_development(self):
        return os.environ["SERVER_SOFTWARE"].startswith("Development")

    def get_user(self):
        self.values['user'] = users.get_current_user()
        if self.values['user']:
            self.values['user_url'] = users.create_logout_url(self.request.url)
        else:
            self.values['user_url'] = users.create_login_url(self.request.url)

    def get_page_array(self):
        page = self.__class__.__name__
        arr = { 'build': 'off', 'learn': 'off', 'about': 'off' }
        if page == "MainPage": arr['build'] = 'on'
        elif page == "LearnPage": arr['learn'] = 'on'
        elif page == "AboutPage": arr['about'] = 'on'
        return arr

    def get(self):
        self.values.update(self.get_values())
        if 'template' in self.values:
            self.values['template'] += ".html"
        else:
            self.values['template'] = self.__class__.__name__.lower() + ".html"
        self.get_user()
        self.values['page'] = self.get_page_array()
        self.values['is_development'] = self.is_development()
        path = os.path.join(os.path.dirname(__file__),
                            '../templates/base.html')
        self.response.out.write(template.render(path, self.values))


class ExtraPage(Page):
    pass


class SessionPage(webapp.RequestHandler):

    def get_session(self):
        if self.request.cookies.has_key("session"):
            cookie = str(self.request.cookies["session"])
            self.session = ui.dao.Session.load(cookie)
            if self.session is not None: return
        self.session = ui.dao.Session.default(self.request.remote_addr)
        self.session.put()
        self.response.headers['Set-Cookie'] = "session=" + self.session.cookie
