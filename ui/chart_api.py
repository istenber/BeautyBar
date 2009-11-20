import logging

from google.appengine.ext import webapp
from model.data import Item, Data
from ui.dao import DAO
from model.session import Session
from model.output import Output
from model.generator_factory import GeneratorFactory

# TODO: refactor session handling into one place
class OutputImage(webapp.RequestHandler):
    def get(self):
        # TODO: use content type from output
        self.response.headers['Content-Type'] = "image/svg+xml"
        if self.request.cookies.has_key("session"):            
            name = str(self.request.cookies["session"])
            session = DAO.load(name=name, class_name="Session")
        g_name = session.style.get_active_generator().name
        self.response.out.write(self._get_generator(session.data, g_name))

    def _get_generator(self, data, name):
        logging.debug("# output_image/_get_generator [" + name + "]")
        gf = GeneratorFactory().instance()
        bars = gf.get_generator(name + ".py")
        bars.scale(0, 50)
        data.to_generator(bars)
        return bars.output()
