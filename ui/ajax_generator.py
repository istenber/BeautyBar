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
        g = self.session.style.get_active_generator()
        gf = GeneratorFactory().instance()
        gen_r = gf.get_generator(g.name + ".py")
        for attr in gen_r.attributes():
            n = attr.x_name()
            i = self.request.get(n)
            if i != "":
                # logging.info("# got \"" + n + "\" as \"" + i + "\"")
                a = g.get_attribute(n)
                # TODO: check that value is valid
                a.value = i
        DAO.save(self.session.style)
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
            part = self._get_html(attr)
            if part is not None:
                parts.append(part)
        values["parts"] = parts
        return values
    
    def _get_html(self, attr):
        part_f = "self._part_" + attr.type()
        if not hasattr(self, "_part_" + attr.type()):
            logging.info("# Unknown attribute \"" + attr.type() +
                         "\" named \"" + attr.x_name() + "\"")
            return None
        else:
            out = ""
            out += self._part_common(attr)
            out += "<td class=\"attr_cell\">"
            out += eval(part_f)(attr)
            out += "</td>\n"
            return out

    def _part_common(self, attr):
        return "<td class=\"attr_cell\">" + attr.name() + "</td>\n"

    def _part_Color(self, attr):
        return ("<input type=\"text\" id=\"" + attr.x_name() + "\"" +
                "maxlength=\"6\" size=\"6\" value=\"" + attr.get() +
                "\" onblur=\"attr.set_color('" + attr.x_name() + "');\">")

    def _part_Boolean(self, attr):
        n = attr.x_name()
        out = ""
        if attr.get(): c = " checked=\"true\""
        else: c = ""
        out += ("Yes:<input type=\"radio\" id=\"" + n + "\"" +
                " name=\"" + n + "\"" + c + " value=\"true\"" +
                " onchange=\"attr.set_boolean('" + n + "', true);\">\n")
        out += " "
        if not attr.get(): c = " checked=\"true\""
        else: c = ""
        out += ("No:<input type=\"radio\" id=\"" + n + "\"" +
                " name=\"" + n + "\"" + c + " value=\"false\"" +
                " onchange=\"attr.set_boolean('" + n + "', false);\">\n")
        return out
