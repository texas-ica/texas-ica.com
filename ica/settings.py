import os


class Config(object):
    SECRET_KEY = os.getenv('SECRET_KEY')
    CSRF_TOKEN = os.getenv('CSRF_TOKEN')
    MAX_CONTENT_LENGTH = 0.5 * 1024 * 1024


class ProductionConfig(Config):
    DEBUG = False
    TESTING = False
    DATABASE_NAME = 'production'
    DATABASE_USER = os.getenv('PROD_DATABASE_USER')
    DATABASE_PASSWORD = os.getenv('PROD_DATABASE_PASSWORD')
    DATABASE_HOST = 'mongodb://ds125481.mlab.com:25481'


class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = True
    DATABASE_NAME = 'development'
    DATABASE_USER = os.getenv('DEV_DATABASE_USER')
    DATABASE_PASSWORD = os.getenv('DEV_DATABASE_PASSWORD')
    DATABASE_HOST = 'mongodb://ds019471.mlab.com:19471'