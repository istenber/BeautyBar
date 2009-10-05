from google.appengine.ext import webapp
from generators.bars import Bars
from model.data import Item, Data
from ui.dao import ItemDAO, DataDAO

class OutputImage(webapp.RequestHandler):
    
    def get(self):
        self.response.headers['Content-Type'] = "image/svg+xml"
        # data = Data.default()
        if self.request.cookies.has_key("session"):            
            session = str(self.request.cookies["session"])
            data = DataDAO.load(session)
        bars = Bars()
        bars.scale(0, 50)
        data.to_generator(bars)
        self.response.out.write(bars.output())

