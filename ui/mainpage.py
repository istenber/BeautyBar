import os
import random
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

class Item(object):

    def __init__(self, name, value):
        self.name  = name
        self.value = value

class MainPage(webapp.RequestHandler):
    
    def get(self):
        if self.request.cookies.has_key("session"):            
            session = str(self.request.cookies["session"])
        else:
            session = str(random.randint(1, 10000000))

        debug = "( session:" + str(session) + " )"
        # debug = "(" + str(dir(self.response)) + ")"
        items = [ Item("Ilpo", "28"),
                  Item("Ilpo", "28"),
                  Item("Lars", "24"),
                  Item("Lars", "24"),
                  Item("Sande", "27"),
                  Item("Sande", "27"),
                  ]
        values = {
            'items' : items,
            'debug' : debug
            }
        path = os.path.join(os.path.dirname(__file__), 
                            '../templates/index.html')
        self.response.headers['Set-Cookie'] = "session=" + session
        self.response.out.write(template.render(path, values))
