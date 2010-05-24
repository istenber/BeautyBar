import logging

from google.appengine.ext import db
from google.appengine.ext import webapp


IMAGE_ROLES = ['other', 'attribute']


class Image(db.Model):

    name = db.StringProperty()
    data = db.BlobProperty()
    role = db.StringProperty(default='other', choices=IMAGE_ROLES)

    @classmethod
    def get_by_name(cls, name):
        return cls.gql("WHERE name = :1", name).get()


class ServeImage(webapp.RequestHandler):

    def image_type_ok(self, name):
        postfix = name[-3:]
        if postfix == "png":
            # TODO: check that is ok!
            self.response.headers['Content-type'] = "image/png"
            return True
        elif postfix == "jpg":
            # TODO: check that is ok!
            # if is_ok...
            self.response.headers['Content-type'] = "image/jpg"
            return True
        else:
            logging.info("incorrect image: " + name)

    def get(self, name):
        if not self.image_type_ok(name):
            self.error(404)
            return
        image = Image.get_by_name(name[:-4])
        if not image:
            logging.info("image not found: " + name)
            self.error(404)
            return
        self.response.out.write(image.data)
            
