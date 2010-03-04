import logging

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
from ui.mainpage import MainPage
from ui.extra_pages import LearnPage, AboutPage
from ui.output_image import PreviewImage, SvgImage, AdminPreviewImage
from ui.data_operations import (CleanData, LoadData, SaveData,
                                ImportData, Dataset)
from ui.ajax_modify import (AjaxModifyName, AjaxModifyValue, AjaxRange,
                            AjaxAddRow, AjaxDelRow)
from ui.ajax_generator import AjaxGenerator, AjaxAttributes, AjaxSetAttribute
from ui.ajax_main import AjaxMain
from ui.chart_api import ChartPage
from ui.gadget import GadgetPage
from ui.feedback import FeedbackProcessor, FeedbackReader
from ui.admin_pages import ViewSessions, AdminMainPage, UploadImage
from ui.error_pages  import MissingPage
from ui.content_preview import ContentPreview
from ui.image import ServeImage
import lib.datastore_cache


import os
is_development = os.environ["SERVER_SOFTWARE"].startswith("Development")


if not is_development:
    lib.datastore_cache.DatastoreCachingShim.Install()
webapp.template.register_template_library('lib.templatetags')


def get_admin_pages():
    # TODO: these should be protected by password...
    return [('/admin/feedback', FeedbackReader),
            ('/admin/sessions', ViewSessions),
            ('/admin/preview', AdminPreviewImage),
            ('/admin/upload_image', UploadImage),
            ('/admin/', AdminMainPage),
            ]

def main():
    if is_development:
        logging.getLogger().setLevel(logging.DEBUG)
    else:
        logging.getLogger().setLevel(logging.INFO)

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
             ('/add_row', AjaxAddRow),
             ('/del_row', AjaxDelRow),

             ('/dataset', Dataset),
             ('/clean', CleanData),
             ('/save', SaveData),
             ('/load', LoadData),
             ('/import_csv', ImportData),

             ('/dbimages/(.*)', ServeImage),

             ('/attr_table', AjaxAttributes),
             ('/chart', ChartPage),
             ('/gadget', GadgetPage),
             ('/feedback', FeedbackProcessor),
             ('/export.svg', SvgImage),
             ('/content_preview', ContentPreview),
             ('/preview', PreviewImage)]
    application = webapp.WSGIApplication(pages +
                                         get_admin_pages() +
                                         [('/.*', MissingPage)],
                                         debug=is_development)
    run_wsgi_app(application)


if __name__ == "__main__":
    main()
