import os


class Config(object):
    SECRET_KEY = os.urandom(32) or 'csn.khai.edu'
    TEMPLATES_AUTO_RELOAD = True
    UPLOADED_IMAGES_DEST = '/images'
