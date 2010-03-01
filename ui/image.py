import logging

from google.appengine.ext import db
from google.appengine.ext import webapp


class Image(db.Model):

    name = db.StringProperty()
    data = db.BlobProperty()

    @classmethod
    def get_by_name(cls, name):
        return cls.gql("WHERE name = :1", name).get()


class ServeImage(webapp.RequestHandler):

    def get(self, name):
        if name[3:] != ".png":
            logging.info("incorrect image: " + name)
            self.error(404)
        image = Image.get_by_name(name[:-4])
        if image:
            self.response.headers['Content-type'] = "image/png"
            self.response.out.write(image.data)
            return 
        else:
            logging.info("image not found: " + name)
            self.error(404)
            
