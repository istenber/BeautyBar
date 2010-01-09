import logging

from google.appengine.ext import webapp
from ui.dao import DAO
from model.session import Session


# TODO: refactor session handling into one place
class ImageBase(webapp.RequestHandler):

    def get(self):
        # TODO: use content type from output
        self.response.headers['Content-Type'] = self.get_content_type()
        self.response.headers['Pragma'] = "no-cache"
        name = self.request.get("session")
        if name == "" and self.request.cookies.has_key("session"):
            name = str(self.request.cookies["session"])
        self.session = DAO.load(name=name, class_name="Session")
        g = self.session.style.get_active_generator()
        self.response.out.write(g.build_chart(self.session.data).output())


class PreviewImage(ImageBase):

    def get_content_type(self):
        return "image/svg+xml"


class SvgImage(ImageBase):

    def get_content_type(self):
        return "application/text"
