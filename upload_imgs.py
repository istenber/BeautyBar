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

# TODO: save image format!?

def dev_passfunc():
    return ('test@example.com', 'nopass')

def production_passfunc():
    import getpass
    return raw_input('Username: '), getpass.getpass('Password: ')

def only_images(filename):
    return filename[-3:] in ['jpg', 'png']

def send_img(name, role):
    filename = IMG_PATH + name
    name = name[:-4]
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
    image.role = role
    image.put()
    logging.debug("sent ok")
    return True

def send_folder(folder, role):
    imgs = filter(only_images, os.listdir(IMG_PATH + '/' + folder))
    for img in imgs:
        if send_img("%s/%s" % (folder, img), role):
            logging.info("%s succeed!!" % img)
        else:
            logging.info("%s failed!!" % img)

def send_bgs():
    send_folder('nature', 'attribute')

def send_popular():
    send_folder('popular', 'popular')

def main():
    # logging.getLogger().setLevel(logging.DEBUG)
    logging.getLogger().setLevel(logging.INFO)
    if not os.path.isdir(IMG_PATH):
        logging.info("missing path %s" % IMG_PATH)
        return
    app_id = "beauty-bar"
    host = "localhost:8080"
    passfunc = dev_passfunc
    if len(sys.argv) != 1:
        mode = sys.argv[1]
        if mode == 'production':
            host = 'beauty-bar.appspot.com'
            passfunc = production_passfunc
        elif mode == 'dev':
            pass
        else:
            logging.info("wrong mode %s" % mode)
            return
    remote_api_stub.ConfigureRemoteDatastore(app_id, 
                                             '/remote_api', 
                                             passfunc,
                                             host)
    # send_img("nature/plains.jpg", 'attribute')
    send_bgs()
    send_popular()

if __name__ == '__main__':
    main()



