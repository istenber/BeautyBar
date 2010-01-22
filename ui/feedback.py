import logging
import os

from google.appengine.ext.webapp import template
from google.appengine.ext import webapp
from google.appengine.ext import db


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


class FeedbackProcessor(webapp.RequestHandler):

    def get_session_id(self):
        if self.request.cookies.has_key("session"):
            return str(self.request.cookies["session"])
        else:
            return "no session found"

    def get(self):
        feedback = self.request.get("feedback")
        user = self.request.get("user")
        if feedback == "": 
            logging.info("# feedback missing.")
        if user == "":
            logging.info("# user missing.")
        fb = Feedback()
        fb.user = user
        fb.message = feedback
        fb.session = self.get_session_id()
        fb.put()        
        self.redirect("/about")

