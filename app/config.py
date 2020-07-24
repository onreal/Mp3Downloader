import os

from dotenv import load_dotenv

# load env
APP_ROOT = os.path.join(os.path.dirname(__file__), '..')
dotenv_path = os.path.join(APP_ROOT, '.env')
load_dotenv(dotenv_path)

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    YT_SEARCH_PAGE = "http://www.youtube.com/results?"
    
    # TODO sensitive connectionString and token should be stored on an environment file
    TELEGRAM_BOT = "899534173:AAHhXMzGdI3mSYGmD_aGDx1AShMrQbWRRyg"
    SECRET_KEY = 'ca64eb3c017dfsdgrthtrt65rhg0539d2b59'
    JWT_SECRET_KEY = 'e5ccc4hthfjhgdfgfdbgfnfdgdsfvfdbdfhadfd45'
    SQLALCHEMY_DATABASE_URI = 'ostgres://username:password@host:port/database'


class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
