import os
import random
import logging

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from ui.data_operations import make_clean_session
from ui.dao import DAO


class BasePage(webapp.RequestHandler):
    
    def _get_values(self):
        """Override me!"""
        
    def get(self):
        if self.request.cookies.has_key("session"):            
            session_name = str(self.request.cookies["session"])
            self.session = DAO.load(name=session_name, class_name="Session")
            if not self.session:
                self.session = make_clean_session()
        else:
            self.session = make_clean_session()
        values = self._get_values()
        if not 'debug' in values:
            values['debug'] = "(none)"
        if 'template' in values:
            values['template'] += ".html"
        else:
            values['template'] = self.__class__.__name__.lower() + ".html"
        path = os.path.join(os.path.dirname(__file__), 
                            '../templates/base.html')
        self.response.headers['Set-Cookie'] = "session=" + self.session.name
        self.response.out.write(template.render(path, values))
