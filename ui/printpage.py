import os

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from ui.basepage import SessionPage


class PrintPage(SessionPage):
    
    def get(self):
        self.get_session()
        values = { 'items' : self.session.data.as_list() }
        path = os.path.join(os.path.dirname(__file__),
                            '../templates/printpage.html')
        self.response.out.write(template.render(path, values))

