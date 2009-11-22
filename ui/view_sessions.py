import logging
import os

from google.appengine.ext.webapp import template
from google.appengine.ext import webapp
from google.appengine.ext import db
from ui.dao import SessionDAO

max_sessions=100

class ViewSessions(webapp.RequestHandler):

    def get(self):
        # TODO: make paging
        daos = SessionDAO.all().fetch(max_sessions)        
        values = {
            'sessions' : daos # TODO: should use Session, not SessionDAO
            }
        path = os.path.join(os.path.dirname(__file__),
                            '../templates/view_sessions.html')
        self.response.out.write(template.render(path, values))
