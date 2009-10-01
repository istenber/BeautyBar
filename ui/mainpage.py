import os
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

class MainPage(webapp.RequestHandler):
    
    def get(self):
        values = {
            'name' : 'ilpo'
            }
        path = os.path.join(os.path.dirname(__file__), '../templates/index.html')
        self.response.out.write(template.render(path, values))
