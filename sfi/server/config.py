from os import getenv, urandom

class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = urandom(16)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = getenv(
        'DATABASE_URL',
        'postgresql://localhost/research_dev'
    )


class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    SECRET_KEY="a-big-secret"


class TestingConfig(Config):
    TESTING = True
