import logging
import os

from google.appengine.ext.webapp import template
from google.appengine.ext import webapp
from google.appengine.ext import db
from ui.basepage import SessionPage


class Feedback(db.Model):

    user = db.StringProperty()
    message = db.TextProperty()
    session = db.StringProperty()


class FeedbackReader(webapp.RequestHandler):

    def get(self):
        values = {
            'feedbacks' : Feedback.all()
            }
        path = os.path.join(os.path.dirname(__file__), 
                            '../templates/feedback_reader.html')
        self.response.out.write(template.render(path, values))  


class FeedbackProcessor(SessionPage):

    def post(self):
        self.get_session()
        feedback = self.request.get("feedback")
        user = self.request.get("user")
        if feedback == "": 
            feedback = "MISSING"
        if user == "":
            user = "MISSING"
        fb = Feedback()
        fb.user = user
        fb.message = feedback
        fb.session = self.session.cookie
        fb.put()
        msg = "Thank you for your feedback."
        self.response.headers['Content-Type'] = "text/plain"
        self.response.out.write("out:" + msg)
