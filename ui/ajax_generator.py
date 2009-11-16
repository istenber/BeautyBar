import logging
import os

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from ui.dao import GeneratorDAO

# TODO: refactor, combine with ajax_modify
class AjaxGenerator(webapp.RequestHandler):
    def get(self):
        # TODO: handle missing args and cookie
        if self.request.cookies.has_key("session"):            
            session = str(self.request.cookies["session"])
        name = self.request.get("name")
        GeneratorDAO.save(session, name)
        self.response.headers['Content-Type'] = "text/plain"
        self.response.out.write("ok.")

class AjaxAttributes(webapp.RequestHandler):
    def get(self):
        # logging.info("# Attribute table called.")
        # TODO: handle missing args and cookie
        if self.request.cookies.has_key("session"):            
            session = str(self.request.cookies["session"])
        values = []
        self.response.headers['Content-Type'] = "text/html"
        path = os.path.join(os.path.dirname(__file__), 
                            '../templates/attribute_table.html')
        self.response.out.write(template.render(path, values))
    
