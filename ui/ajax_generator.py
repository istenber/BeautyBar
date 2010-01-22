import logging
import os

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from model.generator_factory import GeneratorFactory
from ui.ajax_modify import AjaxBase
from model.utils import unquote
import ui.dao

class AjaxGenerator(AjaxBase):

    def real_get(self):
        generator_name = self.request.get("name")
        self.session.style.set_active_generator(generator_name)
        self.session.style.put()
        return "ok."


class AjaxSetAttribute(AjaxBase):

    def real_get(self):
        g = self.session.style.get_active_generator()
        for attr in g.me().get_attributes():
            n = attr.get_name()
            v = unquote(self.request.get(n))
            if v != "":
                # logging.info("# got \"" + n + "\" as \"" + i + "\"")
                # TODO: we cannot do this, or all "random" name variables
                #       turn to be random numbers
                if v == "random":
                    import random
                    import math
                    v = str(int(math.floor(random.random() * 1000 + 0.5)))
                # TODO: check that value is valid
                a = g.get_rw_attribute(n)
                a.value = v
                a.put()
        g.put()
        return "ok."


# TODO: fix to use AjaxHtmlBase or similar
class AjaxAttributes(webapp.RequestHandler):

    def get(self):
        if self.request.cookies.has_key("session"):            
            cookie = str(self.request.cookies["session"])
            self.session = ui.dao.Session.load(cookie)
        values = self.real_get()
        self.response.headers['Content-Type'] = "text/html"
        path = os.path.join(os.path.dirname(__file__),
                            '../templates/attribute_table.html')
        self.response.out.write(template.render(path, values))

    def real_get(self):
        gf = GeneratorFactory().instance()
        g_name = self.session.style.get_active_generator().name
        generator = gf.get_generator(g_name + ".py")
        values = { 'generator_name' : generator.get_ui_name() }
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
                   'value' : attr.get_value(),
                   'attr' : attr,
                   }
        path = os.path.join(os.path.dirname(__file__),
                            '../templates/attributes/' + name + '.html')
        out = ""
        out += "<td class=\"attr_cell\">" + attr.get_ui_name() + "</td>\n"
        out += "<td class=\"attr_cell\">"
        out += template.render(path, values)
        out += "</td>\n"
        return out
