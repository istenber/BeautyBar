from google.appengine.ext import webapp
from google.appengine.ext import db
import generators


FETCHSET = 20


class ReplaceScript(webapp.RequestHandler):

    def get(self):
        self.response.headers['Content-Type'] = "text/plain"      
        count = 0
        q = db.GqlQuery("SELECT from Style")
        offset = 0
        while True:
            styles = q.fetch(FETCHSET, offset=offset)
            offset += FETCHSET
            for style in styles:
                g = style.get_active_generator().me().get_name()
                if not generators.valid(g):
                    count += 1
                    style.set_active_generator('gradient')
                    style.put()
            if len(styles) != FETCHSET:
                self.response.out.write("replaced %d instances" % count)
                return
        return

