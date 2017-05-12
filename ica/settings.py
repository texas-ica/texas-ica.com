import os


class Config(object):
    SECRET_KEY = os.getenv('SECRET_KEY')
    CSRF_TOKEN = os.getenv('CSRF_TOKEN')
    MAX_CONTENT_LENGTH = 0.5 * 1024 * 1024
    CACHE_TYPE = 'filesystem'
    CACHE_THRESHOLD = 128
    CACHE_DIR = '/tmp'


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
    DEBUG_TB_PANELS = (
        'flask_debugtoolbar.panels.versions.VersionDebugPanel',
        'flask_debugtoolbar.panels.timer.TimerDebugPanel',
        'flask_debugtoolbar.panels.headers.HeaderDebugPanel',
        'flask_debugtoolbar.panels.request_vars.RequestVarsDebugPanel',
        'flask_debugtoolbar.panels.template.TemplateDebugPanel',
        'flask_debugtoolbar.panels.logger.LoggingPanel',
        'flask_mongoengine.panels.MongoDebugPanel'
    )
    DEBUG_TB_INTERCEPT_REDIRECTS = False


class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    DATABASE_NAME = 'testing'
    DATABASE_HOST = 'mongodb://127.0.0.1:27017'
    DEBUG_TB_PANELS = (
        'flask_debugtoolbar.panels.versions.VersionDebugPanel',
        'flask_debugtoolbar.panels.timer.TimerDebugPanel',
        'flask_debugtoolbar.panels.headers.HeaderDebugPanel',
        'flask_debugtoolbar.panels.request_vars.RequestVarsDebugPanel',
        'flask_debugtoolbar.panels.template.TemplateDebugPanel',
        'flask_debugtoolbar.panels.logger.LoggingPanel',
        'flask_mongoengine.panels.MongoDebugPanel'
    )
    DEBUG_TB_INTERCEPT_REDIRECTS = False
