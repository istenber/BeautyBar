import logging

from google.appengine.ext import webapp
from model.data import Item, Data
from ui.dao import DAO

class AjaxBase(webapp.RequestHandler):

    def get(self):
        if self.request.cookies.has_key("session"):            
            session_name = str(self.request.cookies["session"])
            self.session = DAO.load(name=session_name, class_name="Session")
            self.data = self.session.data
        out = self.real_get()
        self.response.headers['Content-Type'] = "text/plain"
        self.response.out.write("out:" + str(out))


class AjaxModify(AjaxBase):

    def _handle_scale_update(self):
        min = self.request.get("min")
        max = self.request.get("max")
        if min != "":
            logging.info("# setting min to " + min)
            self.data.set_min(int(min))
            return self.data.min
        if max != "": 
            logging.info("# setting max to " + max)
            self.data.set_max(int(max))
            return self.data.max

    def _handle_data_update(self):
        # TODO: hacky code, needs refactoring...
        x = int(self.request.get("x"))
        y = int(self.request.get("y")) - 1
        val = self.request.get("val")
        # TODO: sanity checks!
        if x == 1: self.data.items[y].name = val
        if x == 2: self.data.items[y].value = val
        return val

    def real_get(self):
        # TODO: handle missing args and cookie
        x_str = self.request.get("x")
        if x_str == "":
            out = self._handle_scale_update()
        else:
            out = self._handle_data_update()
        # TODO: fix bug, session.data is not saved when session is!
        DAO.save(self.session.data)
        return out

