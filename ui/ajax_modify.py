import logging

from django.template.defaultfilters import floatformat
from google.appengine.ext import webapp
from model.data import Item, Data
from ui.basepage import SessionPage
import lib.string_utils
import ui.dao


class AjaxBase(SessionPage):

    def get(self):
        self.get_session()
        self.data = self.session.data
        out = self.real_get()
        self.response.headers['Content-Type'] = "text/plain"
        self.response.out.write("out:" + str(out))


class AjaxAddRow(AjaxBase):

    def real_get(self):
        self.data.add_empty()
        return 0


class AjaxDelRow(AjaxBase):

    def real_get(self):
        self.data.del_last()
        return 0


class AjaxRange(AjaxBase):

    def real_get(self):
        min = self.request.get("min")
        max = self.request.get("max")
        if min != "":
            self.data.set_min(min)
            self.data.put()
            return floatformat(self.data.min)
        if max != "": 
            self.data.set_max(max)
            self.data.put()
            return floatformat(self.data.max)
        return 0


class AjaxModifyName(AjaxBase):

    def real_get(self):
        try:
            row = int(self.request.get("row")) - 1
        except ValueError:
            logging.info("Missing or incorrect row")
            return 0
        item = self.data.get_items()[row]
        val = lib.string_utils.unquote(self.request.get("val"))
        item.set_name(val)
        item.put()
        return item.name


class AjaxModifyValue(AjaxBase):

    def real_get(self):
        try:
            row = int(self.request.get("row")) - 1
        except ValueError:
            logging.info("Missing or incorrect row")
            return 0
        item = self.data.get_items()[row]
        val = lib.string_utils.unquote(self.request.get("val"))
        if ',' in val: val = val.replace(',', '.', 1)
        if not self.data.value_ok(val):
            # Data is out of range.
            # This is valid situation, but we should notify the user anyway.
            # logging.debug("Data out of range")
            return floatformat(item.value)
        item.set_value(val)
        item.put()
        return floatformat(item.value)
