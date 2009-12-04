import logging

from google.appengine.ext import webapp


class MissingPage(webapp.RequestHandler):

    def get(self):
        logging.info("# user tried to reach missing page: " + self.request.url)
        self.redirect("/")
