import os
import logging

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template


class ContentPreview(webapp.RequestHandler):

    def get(self):
        self.response.headers['Content-Type'] = "text/plain"
        self.response.out.write("error, missing content")

    def post(self):
        self.values = []
        path = os.path.join(os.path.dirname(__file__),
                            '../templates/preview.html')
        self.response.out.write(template.render(path, self.values))
