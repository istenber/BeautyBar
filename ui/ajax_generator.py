import logging
import os

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from ui.dao import DAO
from model.generator_factory import GeneratorFactory
from ui.ajax_modify import AjaxBase

class AjaxGenerator(AjaxBase):

    def real_get(self):
        generator_name = self.request.get("name")
        self.session.style.set_active_generator(generator_name)
        DAO.save(self.session.style)
        return "ok."

class AjaxSetAttribute(webapp.RequestHandler):

    def get(self):
        if self.request.cookies.has_key("session"):            
            session = str(self.request.cookies["session"])
        color = self.request.get("bgcolor")
        logging.info("# GOT COLOR " + color)

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
            part_f = "self._part_" + attr.type()
            out = eval(part_f)(attr)
            parts.append(out) # self._part_Color())
        values["parts"] = parts
        self.response.headers['Content-Type'] = "text/html"
        path = os.path.join(os.path.dirname(__file__), 
                            '../templates/attribute_table.html')
        self.response.out.write(template.render(path, values))
    
    def _part_Color(self, attr):
        return ("<tr>\n<td>" + attr.name() + "</td>\n<td>" +
                "<input type=\"text\" id=\"" + attr.x_name() + "\"" +
                " value=\"" + attr.get() + "\" onblur=\"attr.set_color('" +
                attr.x_name() + "');\"></td>\n</tr>")
