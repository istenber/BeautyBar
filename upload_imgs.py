#!/usr/bin/env python2.5

import logging
import sys
import os

DIR_PATH = os.path.abspath('../google_appengine')

EXTRA_PATHS = [
  DIR_PATH,
  os.path.join(DIR_PATH, 'lib', 'antlr3'),
  os.path.join(DIR_PATH, 'lib', 'django'),
  os.path.join(DIR_PATH, 'lib', 'ipaddr'),
  os.path.join(DIR_PATH, 'lib', 'webob'),
  os.path.join(DIR_PATH, 'lib', 'yaml', 'lib'),
]

sys.path = EXTRA_PATHS + sys.path

from google.appengine.ext.remote_api import remote_api_stub
from google.appengine.ext import db

from ui.image import Image
# import ui.dao

IMG_PATH='dynamic_images/'

# TODO: for real server as well...
# TODO: save image format!?

def dev_passfunc():
    return ('test@example.com', 'nopass')

def only_jpgs(filename):
    return ".jpg" in filename

def send_img(name):
    if name.endswith('.jpg'):
        name = name[:-4]
    filename = IMG_PATH + name + '.jpg'
    logging.debug("try to send %s" % name)
    img = Image.gql("WHERE name = :1", name).get()
    if img is not None:
        logging.info("image %s exists" % name)
        return False
    try:
        f = open(filename, 'r')
    except IOError:
        logging.info("missing file %s" % name)
        return False
    data = f.read()
    f.close()
    image = Image()
    image.name = name
    image.data = db.Blob(data)
    image.put()
    logging.debug("sent ok")
    return True

def main():
    # logging.getLogger().setLevel(logging.DEBUG)
    logging.getLogger().setLevel(logging.INFO)
    if not os.path.isdir(IMG_PATH):
        logging.info("missing path %s" % IMG_PATH)
        return
    app_id = "beauty-bar"
    host = "localhost:8080"
    remote_api_stub.ConfigureRemoteDatastore(app_id, 
                                             '/remote_api', 
                                             dev_passfunc, 
                                             host)
    imgs = filter(only_jpgs, os.listdir(IMG_PATH + '/nature'))
    for img in imgs:
        if send_img("nature/%s" % img):
            logging.info("%s succeed!!" % img)
        else:
            logging.info("%s failed!!" % img)


if __name__ == '__main__':
    main()



