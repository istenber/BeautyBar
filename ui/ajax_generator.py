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

class AjaxSetAttribute(AjaxBase):

    def real_get(self):
        color = self.request.get("bgcolor")
        g_name = self.request.get("gen")
        # TODO: make _find_generator public method
        g = self.session.style._find_generator(g_name)
        a = g.get_attribute("bgcolor")
        a.value = color
        DAO.save(self.session.style)
        # TODO: check that value is valid
        return "ok."

# TODO: fix to use AjaxHtmlBase or similar
class AjaxAttributes(webapp.RequestHandler):

    def get(self):
        if self.request.cookies.has_key("session"):            
            session_name = str(self.request.cookies["session"])
            self.session = DAO.load(name=session_name, class_name="Session")
        values = self.real_get()
        self.response.headers['Content-Type'] = "text/html"
        path = os.path.join(os.path.dirname(__file__),
                            '../templates/attribute_table.html')
        self.response.out.write(template.render(path, values))

    def real_get(self):
        gf = GeneratorFactory().instance()
        # TODO: implement missing arg
        g_name = self.request.get("gen")
        if g_name == "session": 
            g_name = self.session.style.get_active_generator().name
        #g_name = self.session.style.get_active_generator().name + ".py"
        generator = gf.get_generator(g_name + ".py")
        values = { 'cur_gen' : g_name }
        parts = []
        for attr in generator.attributes():
            # TODO: select parts for correct attribute type
            #       old value, name and how to handle...
            part_f = "self._part_" + attr.type()
            out = eval(part_f)(attr)
            parts.append(out) # self._part_Color())
        values["parts"] = parts
        return values
    
    def _part_Color(self, attr):
        return ("<tr>\n<td>" + attr.name() + "</td>\n<td>" +
                "<input type=\"text\" id=\"" + attr.x_name() + "\"" +
                " value=\"" + attr.get() + "\" onblur=\"attr.set_color('" +
                attr.x_name() + "');\"></td>\n</tr>")
