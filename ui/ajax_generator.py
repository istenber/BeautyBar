import logging
import os

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from ui.ajax_modify import AjaxBase
import lib.string_utils
import ui.dao


class AjaxGenerator(AjaxBase):

    def real_get(self):
        name = self.request.get("name")
        if self.session.style.set_active_generator(name):
            self.session.style.put()
            return "ok."
        else:
            return "fail."


class AjaxSetAttribute(AjaxBase):

    def real_get(self):
        g = self.session.style.get_active_generator()
        for attr in g.me().get_attributes():
            n = attr.get_name()
            v = lib.string_utils.unquote(self.request.get(n))
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
        g = self.session.style.get_active_generator()
        generator = g.me()
        values = { 'generator_name' : generator.get_ui_name() }
        parts = []
        # TODO: very hackish attribute setting. refactor to better
        ag = self.session.style.get_active_generator()
        for attr in generator.get_attributes():
            val = ag.get_attribute(attr.get_name()).value
            db_val = lib.string_utils.unquote(val)
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
        return ("<td class=\"attr_cell\">" + attr.get_ui_name() + "</td>\n" +
                "<td class=\"attr_cell\">" + template.render(path, values) +
                "</td>\n")
