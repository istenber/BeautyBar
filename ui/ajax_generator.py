import logging
import os

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from ui.dao import DAO
from model.generator_factory import GeneratorFactory
from ui.ajax_modify import AjaxBase
from model.utils import unquote


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
        for attr in gen_r.get_attributes():
            n = attr.get_name()
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
        # TODO: very hackish attribute setting. refactor to better
        ag = self.session.style.get_active_generator()
        for attr in generator.get_attributes():
            db_val = unquote(ag.get_attribute(attr.get_name()).value)
            attr.set_value(db_val)
            part = self._get_html(attr)
            if part is not None:
                parts.append(part)
        values["parts"] = parts
        return values
    
    def _get_html(self, attr):
        name = attr.get_type().lower()
        values = { 'name'  : attr.get_name(),
                   'value' : attr.get_value()
                   }
        path = os.path.join(os.path.dirname(__file__),
                            '../templates/attributes/' + name + '.html')
        out = ""
        out += "<td class=\"attr_cell\">" + attr.get_ui_name() + "</td>\n"
        out += "<td class=\"attr_cell\">"
        out += template.render(path, values)
        out += "</td>\n"
        return out
