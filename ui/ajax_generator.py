from google.appengine.ext import webapp
from ui.dao import GeneratorDAO

class AjaxGenerator(webapp.RequestHandler):
    def get(self):
        # TODO: handle missing args and cookie
        if self.request.cookies.has_key("session"):            
            session = str(self.request.cookies["session"])
        name = self.request.get("name")
        GeneratorDAO.save(session, name)
        self.response.headers['Content-Type'] = "text/plain"
        self.response.out.write("ok.")

