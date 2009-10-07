from google.appengine.ext import webapp
# from model.data import Item, Data
# from ui.dao import ItemDAO, DataDAO

class AjaxModify(webapp.RequestHandler):
    def get(self):
        # data = Data.default()
        # DataDAO.save(data, session)
        self.response.headers['Content-Type'] = "text/plain"
        self.response.out.write("hellou")
