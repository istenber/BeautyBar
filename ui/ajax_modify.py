import logging

from django.template.defaultfilters import floatformat
from google.appengine.ext import webapp
from model.data import Item, Data
from model.utils import unquote
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


class AjaxRange(AjaxBase):

    def real_get(self):
        # TODO: handle missing args and cookie
        min = self.request.get("min")
        max = self.request.get("max")
        if min != "":
            return floatformat(self.data.set_min(min))
        if max != "": 
            return floatformat(self.data.set_max(max))
        # TODO: fix bug, session.data is not saved when session is!
        DAO.save(self.session.data)
        return out


class AjaxModifyName(AjaxBase):

    def real_get(self):
        try:
            row = int(self.request.get("row")) - 1
        except ValueError:
            logging.info("# sometried to use bad row")
            return self.data.items[row].name
        val = unquote(self.request.get("val"))
        self.data.items[row].set_name(val)
        out = self.data.items[row].name
        DAO.save(self.session.data)
        return out


class AjaxModifyValue(AjaxBase):

    def real_get(self):
        try:
            row = int(self.request.get("row")) - 1
        except ValueError:
            logging.info("# sometried to use bad row")
            return floatformat(self.data.items[row].value)
        val = unquote(self.request.get("val"))
        if ',' in val: val = val.replace(',', '.', 1)
        if not self.data.value_ok(val):
            logging.info("# some tries to send data out of range")
            # TODO: raise error?
            return floatformat(self.data.items[row].value)
        self.data.items[row].set_value(val)
        out = self.data.items[row].value
        DAO.save(self.session.data)
        return floatformat(out)
