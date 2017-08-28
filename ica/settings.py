import os


class Config(object):
    SECRET_KEY = os.getenv('SECRET_KEY')
    CSRF_TOKEN = os.getenv('CSRF_TOKEN')
    CACHE_TYPE = 'redis'
    CACHE_REDIS_URL = os.getenv('REDISCLOUD_URL')
    SLACK_API_KEY = os.getenv('SLACK_API_KEY')


class ProductionConfig(Config):
    DEBUG = False
    TESTING = False
    DATABASE_NAME = 'production'
    DATABASE_USER = os.getenv('PROD_DATABASE_USER')
    DATABASE_PASSWORD = os.getenv('PROD_DATABASE_PASSWORD')
    DATABASE_HOST = os.getenv('PROD_DATABASE_HOST')


class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = True
    DATABASE_NAME = 'heroku_b694ljx0'
    DATABASE_USER = os.getenv('DEV_DATABASE_USER')
    DATABASE_PASSWORD = os.getenv('DEV_DATABASE_PASSWORD')
    DATABASE_HOST = os.getenv('DEV_DATABASE_HOST')
    CACHE_REDIS_URL = os.getenv('DEV_REDISCLOUD_URL')
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
    DATABASE_USER = None
    DATABASE_PASSWORD = None
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
