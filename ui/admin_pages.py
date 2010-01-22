import logging
import os

from google.appengine.ext.webapp import template
from google.appengine.ext import webapp
from google.appengine.ext import db
import ui.dao


max_sessions=100


class ViewSessions(webapp.RequestHandler):

    def get(self):
        # TODO: make paging
        sessions = ui.dao.Session.all().fetch(max_sessions)        
        values = {
            'sessions' : sessions
            }
        path = os.path.join(os.path.dirname(__file__),
                            '../templates/view_sessions.html')
        self.response.out.write(template.render(path, values))


class AdminMainPage(webapp.RequestHandler):

    def get(self):
        values = {}
        path = os.path.join(os.path.dirname(__file__),
                            '../templates/admin.html')
        self.response.out.write(template.render(path, values))
