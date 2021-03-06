import logging
import os

from google.appengine.ext.webapp import template
from google.appengine.ext import webapp
from google.appengine.ext import db
from ui.image import Image
import ui.dao


PAGESIZE = 20


class ViewSessions(webapp.RequestHandler):

    def get(self):
        page = self.request.get("page")
        if page == "":
            page = 1
        else:
            try:
                page = int(page)
            except ValueError:
                logging.info("Incorrect page: " + page)
                page = 1
        offset = (page - 1) * PAGESIZE
        sessions = ui.dao.Session.all().fetch(PAGESIZE + 1, offset=offset)
        if len(sessions) > PAGESIZE:
            next_page = page + 1
        else:
            next_page = None
        if page > 1:
            prev_page = page - 1
        else:
            prev_page = None
        values = {
            'sessions' : sessions[:PAGESIZE],
            'next_page' : next_page,
            'prev_page' : prev_page,
            }
        path = os.path.join(os.path.dirname(__file__),
                            '../templates/view_sessions.html')
        self.response.out.write(template.render(path, values))


class AdminMainPage(webapp.RequestHandler):

    def get(self):
        values = { 'image' : self.request.get("image") }
        path = os.path.join(os.path.dirname(__file__),
                            '../templates/admin.html')
        self.response.out.write(template.render(path, values))




class UploadImage(webapp.RequestHandler):

    def post(self):
        data = self.request.get("img_data")
        name = self.request.get("img_name")
        if data == "":
            logging.info("image upload missing data")
        elif name == "":
            logging.info("image upload missing name")
        else:
            image = Image()
            image.name = name
            image.data = db.Blob(data)
            image.put()
        self.redirect("/admin/?image=" + name)
