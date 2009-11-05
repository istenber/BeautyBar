import os
import random
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

class BasePage(webapp.RequestHandler):
    
    def _get_values(self):
        """Override me!"""
        
    def get(self):
        if self.request.cookies.has_key("session"):            
            session = str(self.request.cookies["session"])
        else:
            # TODO: should use data_operations.py / CleanData
            session = str(random.randint(1, 10000000))

        values = self._get_values()
        if not 'debug' in values:
            values['debug'] = "(none)"
        #    'template'   : "learnpage.html", # TODO:
        path = os.path.join(os.path.dirname(__file__), 
                            '../templates/base.html')
        self.response.headers['Set-Cookie'] = "session=" + session
        self.response.out.write(template.render(path, values))    

class LearnPage(BasePage):
    
    def _get_values(self):
        return { 'template' : "learnpage.html" }

class InfoPage(BasePage):
    
    def _get_values(self):
        return { 'template' : "infopage.html" }
