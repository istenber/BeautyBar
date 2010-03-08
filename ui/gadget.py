import logging

from google.appengine.ext import webapp
from google.appengine.api import memcache
from ui.chart_api import ApiPage
import lib.string_utils
import ui.dao


class GadgetPage(ApiPage):

    def get_chart_params(self):
        return { 'size': "size", 'style': "style" }

    def _has_x(self, x):
        value = self.request.get(x)
        if value == "": return False
        setattr(self, x, lib.string_utils.unquote(value))
        return True

    def has_datasource(self):
        return self._has_x("datasource")

    def has_datastring(self):
        return self._has_x("datastring")

    def get_data(self):
        if self.has_datasource():
            # TODO: enable datasource support
            self.data_error = "Datasource option not supported"
            return ""
        if self.has_datastring():
            data = ui.dao.Data.from_datastring(self.datastring)
            if data is None:
                self.data_error = "Cannot parse data"
                return ""
            return data
        self.data_error = "Missing data"
        return ""

