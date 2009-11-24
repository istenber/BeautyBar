import logging
import os

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from ui.dao import DAO
from model.generator_factory import GeneratorFactory

class AjaxMain(webapp.RequestHandler):

    def _is_valid_part(self, part):
        return part in ['list', 'info', 'edit']

    def get(self):
        part = self.request.get("part")
        if not self._is_valid_part(part):
            self.response.headers['Content-Type'] = "text/plain"
            logging.info("# Trying get invalid part \"" + str(part) + "\"")
            self.response.out.write("error")
            return
        if self.request.cookies.has_key("session"):            
            session_name = str(self.request.cookies["session"])
            self.session = DAO.load(name=session_name, class_name="Session")
        values = eval("self.get_" + part)()
        self.response.headers['Content-Type'] = "text/html"
        file = "../templates/main/" + values['template'] + ".html"
        path = os.path.join(os.path.dirname(__file__), file)
        self.response.out.write(template.render(path, values))

    # TODO: implement part caching in javascript

    def get_list(self):
        return { 'template' : 'list' }

    def get_info(self):
        return { 'template' : 'info' }

    def get_edit(self):
        return { 'template' : 'edit' }
