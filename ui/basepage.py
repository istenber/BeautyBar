import os
import random
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from ui.data_operations import make_clean_session

class BasePage(webapp.RequestHandler):
    
    def _get_values(self):
        """Override me!"""
        
    def get(self):
        if self.request.cookies.has_key("session"):            
            self.session = str(self.request.cookies["session"])
        else:
            ses = make_clean_session()
            self.session = ses.name

        values = self._get_values()
        if not 'debug' in values:
            values['debug'] = "(none)"        
        values['template'] = self.__class__.__name__.lower() + ".html"

        path = os.path.join(os.path.dirname(__file__), 
                            '../templates/base.html')
        self.response.headers['Set-Cookie'] = "session=" + self.session
        self.response.out.write(template.render(path, values))
