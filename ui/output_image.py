import logging

from google.appengine.ext import webapp
from ui.dao import DAO
from model.session import Session
from model.generator_factory import GeneratorFactory

# TODO: refactor session handling into one place
class OutputImage(webapp.RequestHandler):

    def _unquote(self, string):
        if string.startswith('"') : string = string[1:]
        if string.endswith('"') : string = string[:-1]
        return string

    def get(self):
        # TODO: use content type from output
        self.response.headers['Content-Type'] = "image/svg+xml"
        name = self.request.get("session")
        if name == "" and self.request.cookies.has_key("session"):
            name = str(self.request.cookies["session"])
        self.session = DAO.load(name=name, class_name="Session")
        self.response.out.write(self._get_generator())

    def _get_generator(self):
        g = self.session.style.get_active_generator()
        gf = GeneratorFactory().instance()
        chart = gf.get_generator(g.name + ".py")
        for attr in chart.attributes():
            v = self._unquote(g.get_attribute(attr.x_name()).value)
            attr.set(v)
        self.session.data.to_generator(chart)
        return chart.output()
