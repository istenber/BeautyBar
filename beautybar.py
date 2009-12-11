import logging

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
from ui.mainpage import MainPage
from ui.extra_pages import LearnPage, AboutPage
from ui.output_image import OutputImage
from ui.data_operations import CleanData, LoadData, SaveData, ImportData
from ui.ajax_modify import AjaxModifyName, AjaxModifyValue, AjaxRange
from ui.ajax_generator import AjaxGenerator, AjaxAttributes, AjaxSetAttribute
from ui.ajax_main import AjaxMain
from ui.chart_api import ChartPage
from ui.feedback import FeedbackProcessor, FeedbackReader
from ui.admin_pages import ViewSessions, AdminMainPage
from ui.error_pages  import MissingPage

def get_admin_pages():
    # TODO: these should be protected by password...
    return [('/admin/feedback', FeedbackReader),
            ('/admin/sessions', ViewSessions),
            ('/admin/', AdminMainPage),
            ]

def main():
    # TODO: use environment variable "debug"
    debug=True
    if debug:
        from ui.test.dao import TestDao
        test_pages = [('/test/dao', TestDao)]
        log_level = logging.DEBUG
    else:
        test_pages = []
        log_level = logging.INFO
    logging.getLogger().setLevel(log_level)

    # TODO: split pages to groups: infopages, normalpages, ajaxpages, etc.
    pages = [('/', MainPage),
             ('/main', AjaxMain),

             ('/about', AboutPage),
             ('/learn', LearnPage),

             ('/set_name', AjaxModifyName),
             ('/set_value', AjaxModifyValue),
             ('/set_range', AjaxRange),
             ('/set_generator', AjaxGenerator),
             ('/set_attr', AjaxSetAttribute),

             ('/clean', CleanData),
             ('/save', SaveData),
             ('/load', LoadData),
             ('/import_csv', ImportData),

             ('/attr_table', AjaxAttributes),
             ('/chart', ChartPage),
             ('/feedback', FeedbackProcessor),
             ('/output_image', OutputImage)]
    application = webapp.WSGIApplication(pages +
                                         test_pages +
                                         get_admin_pages() +
                                         [('/.*', MissingPage)],
                                         debug=debug)
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
