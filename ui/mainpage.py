import os
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

class Item(object):

    def __init__(self, name, value):
        self.name  = name
        self.value = value

class MainPage(webapp.RequestHandler):
    
    def get(self):
        values = {
            'name'  : 'ilpo',
            'items' : [ Item("Ilpo", "28"),
                        Item("Ilpo", "28"),
                        Item("Lars", "24"),
                        Item("Lars", "24"),
                        Item("Sande", "27"),
                        Item("Sande", "27"),
                        ],
            }
        path = os.path.join(os.path.dirname(__file__), 
                            '../templates/index.html')
        self.response.out.write(template.render(path, values))
