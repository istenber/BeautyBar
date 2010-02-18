import logging

from google.appengine.ext import webapp
from google.appengine.api import memcache
from model.generator_factory import GeneratorFactory
from lib.google_datasource import GoogleDataSource
from model.data import Data
from model.utils import unquote
import ui.dao


# TODO: this is (modified) copy of chart_api.py, so we need to
#       refactor these to use common codebase.
# TODO: output should be png image!
class GadgetPage(webapp.RequestHandler):

    # example
    # http://localhost:8080/gadget?size=500x400&style=plain&datasource="http://spreadsheets.google.com/tq?range=B5:C10&headers=-1&key=0Al2-SsPjGtFbdGwyemZZVjk2SGNzRHBCTUQyRjdqTmc&gid=0"

    def _default_style(self, msg):
        logging.info(msg)
        return ui.dao.Style.default()

    def _get_style(self):
        filename = self.request.get("style")
        if filename == "": return self._default_style("Missing style")
        # TODO: now style loading is based on session, fix it to
        #       use style when there is style naming
        session = ui.dao.Session.load_file(filename)
        if session is None:
            return self._default_style("Session \"" + filename + "\" not found")
        s = session.style
        if s is None:
            return self._default_style("Style not found")
        return s

    def _convert_ampersand(self, text):
        return text.replace('_amp_', '&')

    def _default_data(self, msg):
        logging.info("# " + msg)
        return ui.dao.Data.default()

    def _get_data(self):
        datasource = unquote(self.request.get("datasource"))
        if datasource == "": return self._default_data("Missing datasource")
        datasource = self._convert_ampersand(datasource)
        ds = GoogleDataSource()
        ds.set_source(datasource)
        if not ds.is_ok(): return self._default_data("Broken datasource: " +
                                                     datasource)
        d = Data.read_datasource(ds)
        if d == None: self._default_data("Incorrect (size?) datasource")
        return d

    def _get_size(self):
        size = self.request.get("size")
        if size == "":
            logging.debug("Using default chart size 300x200")
            size = "300x200"
        return size

    def cache_key(self):
        key = ""
        for arg in self.request.arguments():
            key += arg + "=" + self.request.get(arg) + "&"
        key = key[:-1]
        logging.debug("Memcache key: " + key)
        return key

    def in_cache(self, key):
        self.cached_data = memcache.get(key)
        return self.cached_data is not None

    def get(self):
        self.response.headers['Content-Type'] = "image/svg+xml"
        key = self.cache_key()
        if False: # self.in_cache(key):
            logging.debug("Found in cache")
            out = self.cached_data
        else:
            s = self._get_style()
            d = self._get_data()
            g = s.get_active_generator()
            chart = g.build_chart(d)
            size = self._get_size()
            chart.resize_str(size)
            out = chart.output()
            memcache.add(key, out)
        self.response.out.write(out)