import logging

from google.appengine.ext import webapp
from model.data import Item, Data
from ui.dao import ItemDAO, DataDAO

default_generator="shiny"

class OutputImage(webapp.RequestHandler):    
    def get(self):
        name = self.request.get("name")
        if name == "": name = default_generator
        logging.debug("# generator name(" + name + ")")
        self.response.headers['Content-Type'] = "image/svg+xml"
        if self.request.cookies.has_key("session"):            
            session = str(self.request.cookies["session"])
            data = DataDAO.load(session)
        self.response.out.write(self._get_generator(data, name))

    def _get_generator(self, data, name):
        logging.debug("# output_image/_get_generator [" + name + "]")
        # TODO: verify that generator exists...
        classname = name.capitalize()
        filename = "generators." + name
        import_cmd = "from " + filename + " import " + classname
        logging.info(import_cmd)
        exec(import_cmd)
        bars = eval(classname + "()")
        bars.scale(0, 50)
        data.to_generator(bars)
        return bars.output()
