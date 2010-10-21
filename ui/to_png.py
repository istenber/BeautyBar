import logging

from google.appengine.ext import webapp
from ui.basepage import SessionPage
from google.appengine.api.urlfetch_errors import DownloadError
import ui.dao

from StringIO import StringIO
import urllib2, urllib, lib.MultipartPostHandler
import time


IMAGE_SERVER_URL = "http://localhost:8000"
DEFAULT_PNG_WIDTH = 300
DEFAULT_PNG_HEIGHT = 200


def get_upload_url(data):
    """ get form url """
    from HTMLParser import HTMLParser
    class CustomParser(HTMLParser):
        def handle_starttag(self, tag, attrs):
            if tag == "form":
                for (key, name) in attrs:
                    if key == "action":
                        self.form_url = name
    parser = CustomParser()
    parser.feed(data)
    return parser.form_url

def send_svg(data, width, height, debug=False):
    tries = 5
    while tries > 0:
        try:
            mainpage = urllib2.urlopen(IMAGE_SERVER_URL)
            break
        except urllib2.URLError:
            logging.info("urlerror: waiting image server")
            time.sleep(1)
            tries -= 1
        except DownloadError:
            logging.info("downloaderror: waiting image server")
            time.sleep(1)
            tries -= 1
    upload_url = IMAGE_SERVER_URL + get_upload_url(mainpage.read())
    params = { "width" : str(width),
               "height" : str(height),
               "debug" : "true" if debug else "false",
               "file" : StringIO(data) }
    opener = urllib2.build_opener(lib.MultipartPostHandler.MultipartPostHandler)
    try:
        f = opener.open(upload_url, params)
    except DownloadError, err:
        logging.error("failed get img: " + str(err))
        return None
    return f.read()


class ToPng(SessionPage):

    def set_image_size(self):
        try:
            self.png_width = int(self.request.get("width"))
        except ValueError:
            self.png_width = DEFAULT_PNG_WIDTH
        try:
            self.png_height = int(self.request.get("height"))
        except ValueError:
            self.png_height = DEFAULT_PNG_HEIGHT

    def get(self):
        self.get_session()
        # to let browsers to download image instead of showing it,
        # we use application/text mime type
        self.response.headers['Content-Type'] = "image/png"
        # self.response.headers['Content-Type'] = "application/text"
        self.set_image_size()
        g = self.session.style.get_active_generator()
        out = g.build_chart(self.session.data).output()        
        png_data = send_svg(out, self.png_width, self.png_height)
        if (png_data is None) or (len(png_data) == 0):            
            self.redirect("/images/pngerror.png")
        else:
            self.response.out.write(png_data)
