import logging

from google.appengine.ext import webapp
from ui.dao import DAO
from model.session import Session


# TODO: refactor session handling into one place
class OutputImage(webapp.RequestHandler):

    def get(self):
        # TODO: use content type from output
        self.response.headers['Content-Type'] = "image/svg+xml"
        name = self.request.get("session")
        if name == "" and self.request.cookies.has_key("session"):
            name = str(self.request.cookies["session"])
        self.session = DAO.load(name=name, class_name="Session")
        g = self.session.style.get_active_generator()
        self.response.out.write(g.build_chart(self.session.data))
