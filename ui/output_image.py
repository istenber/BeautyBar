import logging
# TODO: encoding disabled, as app engine does not support it
# import gzip
# from StringIO import StringIO

from google.appengine.ext import webapp
from ui.dao import DAO
from model.session import Session


# TODO: refactor session handling into one place
class ImageBase(webapp.RequestHandler):

    # from http://jython.xhaus.com/http-compression-in-python-and-jython/
    def compressBuf(self, buf):
        zbuf = StringIO()
        zfile = gzip.GzipFile(mode = 'wb',  fileobj = zbuf, compresslevel = 9)
        zfile.write(buf)
        zfile.close()
        return zbuf.getvalue()

    def encode(self, string):
        try:
            enc = self.request.headers['Accept-Encoding']
        except KeyError:
            return string
        if "gzip" in enc:
            self.response.headers['Transfer-Encoding'] = "gzip"
            return self.compressBuf(string)
        return string

    def get(self):
        # TODO: use content type from output
        self.response.headers['Content-Type'] = self.get_content_type()
        self.response.headers['Pragma'] = "no-cache"
        name = self.request.get("session")
        if name == "" and self.request.cookies.has_key("session"):
            name = str(self.request.cookies["session"])
        self.session = DAO.load(name=name, class_name="Session")
        g = self.session.style.get_active_generator()
        # TODO: encoding disabled, as app engine does not support it
        # out = self.encode(g.build_chart(self.session.data).output())
        out = g.build_chart(self.session.data).output()
        self.response.out.write(out)


class PreviewImage(ImageBase):

    def get_content_type(self):
        return "image/svg+xml"


class SvgImage(ImageBase):

    def get_content_type(self):
        return "application/text"
