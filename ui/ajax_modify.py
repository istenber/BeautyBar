from google.appengine.ext import webapp
from model.data import Item, Data
from ui.dao import ItemDAO, DataDAO

class AjaxModify(webapp.RequestHandler):
    def get(self):
        # TODO: handle missing args and cookie
        if self.request.cookies.has_key("session"):            
            session = str(self.request.cookies["session"])
            data = DataDAO.load(session)
        x = int(self.request.get("x"))
        y = int(self.request.get("y")) - 1
        val = self.request.get("val")
        if x == 1:
            item = Item(val, data.items[y].value)
            out = item.name
        if x == 2:
            item = Item(data.items[y].name, val)
            out = item.value
        data.items[y] = item
        DataDAO.save(data, session)
        self.response.headers['Content-Type'] = "text/plain"
        # TODO: return something useful
        self.response.out.write("out:" + str(out))
