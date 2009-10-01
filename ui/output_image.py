from google.appengine.ext import webapp

class OutputImage(webapp.RequestHandler):
    
    def get(self):
        self.response.headers['Content-Type'] = "image/svg+xml"
        with open("generators/bars/template.svg") as f:
            out = f.read()
        self.response.out.write(out)
