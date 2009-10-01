from google.appengine.ext import webapp
from generators.bars import Bars

class OutputImage(webapp.RequestHandler):
    
    def get(self):
        # self.response.headers['Content-Type'] = "image/svg+xml"
        bars = Bars()
        bars.scale(0, 50)
        bars.add("Ilpo", 28)
        bars.add("Lasse", 24)
        bars.add("Sanna", 27)
        bars.add("Ilpo", 28)
        bars.add("Lasse", 24)
        bars.add("Sanna", 27)
        self.response.out.write(bars.output())
        # self.response.out.write(bars.output())
