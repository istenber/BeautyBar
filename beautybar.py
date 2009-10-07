from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
from ui.mainpage import MainPage
from ui.output_image import OutputImage
from ui.data_operations import CleanData
from ui.ajax_modify import AjaxModify

application = webapp.WSGIApplication([('/', MainPage),
                                      ('/modify_data', AjaxModify),
                                      ('/clean', CleanData),
                                      ('/output_image', OutputImage)],
                                      debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
