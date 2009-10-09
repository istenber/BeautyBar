import logging

from google.appengine.ext import webapp
from model.data import Item, Data
from ui.dao import ItemDAO, DataDAO

class OutputImage(webapp.RequestHandler):
    
    def get(self):
        generator = self.request.get("generator")
        if generator == "":
            generator = "bars"
        logging.info("generator(" + generator + ")")
        self.response.headers['Content-Type'] = "image/svg+xml"
        if self.request.cookies.has_key("session"):            
            session = str(self.request.cookies["session"])
            data = DataDAO.load(session)
        if hasattr(self, "_" + generator):
            f = getattr(self, "_" + generator)
        self.response.out.write(f(data))

    def _bars(self, data):
        x = "bars"
        classname = x.capitalize()
        filename = "generators." + x
        import_cmd = "from " + filename + " import " + classname
        logging.info(import_cmd)
        exec(import_cmd)
        bars = Bars()
        bars.scale(0, 50)
        data.to_generator(bars)
        return bars.output()

