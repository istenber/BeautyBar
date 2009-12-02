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
            # logging.info("# setting min to " + min)
            return self.data.set_min(min)
        if max != "": 
            # logging.info("# setting max to " + max)
            return self.data.set_max(max)

    def _handle_data_update(self):
        # TODO: hacky code, needs refactoring...
        x = int(self.request.get("x"))
        y = int(self.request.get("y")) - 1
        val = self.request.get("val")
        if x == 1:
            self.data.items[y].set_name(val)
            return self.data.items[y].name
        if x == 2:
            if ',' in val: val.replace(',', '.', 1)
            if self.data.value_ok(val):
                self.data.items[y].set_value(val)
            from django.template.defaultfilters import floatformat
            return floatformat(self.data.items[y].value)
        logging.info("# some tries to send data out of range")
        return "failed." # TODO: raise error?

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

