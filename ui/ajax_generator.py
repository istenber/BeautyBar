import logging
import os

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from ui.dao import GeneratorDAO
from model.generator_factory import GeneratorFactory

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
        # TODO: handle missing args and cookie
        if self.request.cookies.has_key("session"):            
            session = str(self.request.cookies["session"])
        gen_name = GeneratorDAO.load(session)
        gf = GeneratorFactory().instance()
        generator = gf.get_generator(gen_name + ".py")
        values = {}
        parts = []
        for attr in generator.attributes():
            # TODO: select parts for correct attribute type
            #       old value, name and how to handle...
            parts.append(self._part_Color())
        values["parts"] = parts
        self.response.headers['Content-Type'] = "text/html"
        path = os.path.join(os.path.dirname(__file__), 
                            '../templates/attribute_table.html')
        self.response.out.write(template.render(path, values))
    
    def _part_Color(self):
        return ("<tr>\n<td>Color:</td>\n<td>" +
                "<input type=\"text\" name=\"bgcolor\" value=\"red\">\n" +
                "</td></tr>")
