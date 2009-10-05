import os
import random
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

from model.data import Item, Data

#class Item(object):

#     def __init__(self, name, value):
#         self.name  = name
#         self.value = value

# TODO: make clean/new button

# TODO: store and read data from db based on session

# TODO: make data fields editable with ajax

class MainPage(webapp.RequestHandler):
    
    def get(self):
        if self.request.cookies.has_key("session"):            
            session = str(self.request.cookies["session"])
        else:
            session = str(random.randint(1, 10000000))

        data = Data.default()
        items = data.as_list()
        # debug = "( data:" + str(data.as_list()) + " )"
        # debug = "( session:" + str(session) + " )"
        # debug = "(" + str(dir(self.response)) + ")"
        debug = "(none)"
        values = {
            'items' : items,
            'debug' : debug
            }
        path = os.path.join(os.path.dirname(__file__), 
                            '../templates/index.html')
        self.response.headers['Set-Cookie'] = "session=" + session
        self.response.out.write(template.render(path, values))
