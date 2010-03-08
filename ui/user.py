import logging
import os

from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template


class User(db.Model):
    user = db.UserProperty()
    sessions = db.StringListProperty()

    @classmethod
    def get_user(cls, user):
        return cls.gql("WHERE user = :1", user).get()


class UserStats(object):

    def __init__(self, user, cookie):
        u = User.get_user(user)
        if u is None:
            u = User()
            u.user = user
        if cookie not in u.sessions:
            u.sessions.append(cookie)
        u.put()


class UserViewer(webapp.RequestHandler):

    def get(self):
        values = {
            'users' : User.all()
            }
        path = os.path.join(os.path.dirname(__file__), 
                            '../templates/user_viewer.html')
        self.response.out.write(template.render(path, values))  
