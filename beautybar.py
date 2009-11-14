import logging

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
from ui.mainpage import MainPage
from ui.extra_pages import LearnPage, InfoPage
from ui.output_image import OutputImage
from ui.data_operations import CleanData, LoadData, SaveData, ImportData
from ui.ajax_modify import AjaxModify
from ui.ajax_generator import AjaxGenerator

application = webapp.WSGIApplication([('/', MainPage),
                                      ('/info', InfoPage),
                                      ('/learn', LearnPage),
                                      ('/modify_data', AjaxModify),
                                      ('/set_generator', AjaxGenerator),
                                      ('/clean', CleanData),
                                      ('/save', SaveData),
                                      ('/load', LoadData),
                                      ('/import_csv', ImportData),
                                      ('/output_image', OutputImage)],
                                     debug=True)

def main():
    logging.getLogger().setLevel(logging.INFO)
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
