import os
import random
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

class LearnPage(webapp.RequestHandler):
    
    def get(self):
        # TODO: move to general functions or derive all pages
        #       from SessionPage?
        if self.request.cookies.has_key("session"):            
            session = str(self.request.cookies["session"])
        else:
            # TODO: should use data_operations.py / CleanData
            session = str(random.randint(1, 10000000))
        debug = "(none)"
        values = {
            'template'   : "learnpage.html",
            'debug'      : debug,
            }
        path = os.path.join(os.path.dirname(__file__), 
                            '../templates/base.html')
        self.response.headers['Set-Cookie'] = "session=" + session
        self.response.out.write(template.render(path, values))

class InfoPage(webapp.RequestHandler):
    
    def get(self):
        # TODO: move to general functions or derive all pages
        #       from SessionPage?
        if self.request.cookies.has_key("session"):            
            session = str(self.request.cookies["session"])
        else:
            # TODO: should use data_operations.py / CleanData
            session = str(random.randint(1, 10000000))
        debug = "(none)"
        values = {
            'template'   : "infopage.html",
            'debug'      : debug,
            }
        path = os.path.join(os.path.dirname(__file__), 
                            '../templates/base.html')
        self.response.headers['Set-Cookie'] = "session=" + session
        self.response.out.write(template.render(path, values))
