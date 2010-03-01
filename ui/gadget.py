import logging

from google.appengine.ext import webapp
from google.appengine.api import memcache
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

    def _get_ds_headers(self):
        if self.request.headers.has_key('Referer'):
            return { 'Referer' : self.request.headers['Referer'] }
        return None

    def _default_data(self, msg):
        logging.info(msg)
        return (None, ui.dao.Data.default())

    def _get_signature_and_data(self):
        datasource = unquote(self.request.get("datasource"))
        if datasource == "": return self._default_data("Missing datasource")
        datasource = self._convert_ampersand(datasource)
        ds = GoogleDataSource()
        ds.set_source(datasource, self._get_ds_headers())
        if not ds.is_ok(): return self._default_data("Broken datasource: " +
                                                     datasource)
        d = Data.read_datasource(ds)
        if d == None: self._default_data("Incorrect (size?) datasource")
        return (ds.get_signature(), d)

    def _get_size(self):
        size = self.request.get("size")
        if size == "":
            logging.debug("Using default chart size 300x200")
            size = "300x200"
        return size

    def cache_key(self, extras=[]):
        key = ""
        for arg in self.request.arguments():
            if arg == 'rnd': continue
            key += arg + "=" + self.request.get(arg) + "&"
        key = key[:-1]
        for extra in extras:
            key += "$" + str(extra)
        logging.debug("Memcache key: " + key)
        return key

    def in_cache(self, key):
        self.cached_data = memcache.get(key)
        return self.cached_data is not None

    def get(self):
        self.response.headers['Content-Type'] = "image/svg+xml"
        (signature, d) = self._get_signature_and_data()
        caching = (signature is not None)
        if caching:
            key = self.cache_key([signature])
            if self.in_cache(key):
                logging.debug("Found in cache")
                self.response.out.write(self.cached_data)
                return
        g = self._get_style().get_active_generator()
        chart = g.build_chart(d)
        chart.resize_str(self._get_size())
        out = chart.output()
        if caching:
            memcache.add(key, out)
        self.response.out.write(out)
