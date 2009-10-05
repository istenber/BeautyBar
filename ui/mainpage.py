import os
import random
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from model.data import Item, Data
from ui.dao import ItemDAO, DataDAO

# TODO: store and read data from db based on session
# TODO: make data fields editable with ajax

class MainPage(webapp.RequestHandler):
    
    def get(self):
        debug = "(none)"
        if self.request.cookies.has_key("session"):            
            session = str(self.request.cookies["session"])
            data = DataDAO.load(session)
        else:
            # TODO: should use data_operations.py / CleanData
            session = str(random.randint(1, 10000000))
            data = Data.default()
            DataDAO.save(data, session)

        items = data.as_list()
        # debug = "( data:" + str(data.as_list()) + " )"
        debug = "( session:" + str(session) + " )"
        # debug = "(" + str(dir(self.response)) + ")"

        values = {
            'items' : items,
            'debug' : debug
            }
        path = os.path.join(os.path.dirname(__file__), 
                            '../templates/index.html')
        self.response.headers['Set-Cookie'] = "session=" + session
        self.response.out.write(template.render(path, values))
