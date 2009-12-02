import logging
import os

from google.appengine.ext.webapp import template
from google.appengine.ext import webapp
from google.appengine.ext import db
from ui.dao import DAO

# TODO: should we use DAO based db model?
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

    # TODO: move _send_message to somewhere common methods!!

    # TODO: implement reading and storing to database somewhere
    def _send_message(self, msg):
        self.session.message = msg
        # TODO: save message: DAO.save(session)

    def get(self):
        feedback = self.request.get("feedback")
        user = self.request.get("user")        
        if self.request.cookies.has_key("session"):
            name = str(self.request.cookies["session"])
            self.session = DAO.load(name=name, class_name="Session")
        if feedback == "": 
            logging.info("# feedback missing.")
            self.redirect("/about")
        if user == "": logging.info("# user missing.")
        fb = Feedback()
        fb.user = user
        fb.message = feedback
        fb.session = self.session.name
        fb.put()        
        self._send_message("Feedback sent.")
        # TODO: redirect to page where message was sent
        self.redirect("/about")

