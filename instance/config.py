# /instance/config.py
# Flask needs some sought of configuration to be available before the app starts. 
# Since environments (development, production or testing) require specific settings to be configured, 
# we'll have to set environment-specific things such as a secret key, debug mode and test mode 
# in our configurations file.

import os


class Config(object):
    """Parent configuration class."""
    DEBUG = False
    CSRF_ENABLED = True
    SECRET = os.getenv('SECRET')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')

class ProductionConfig(Config):
    """Configurations for Production."""
    DEBUG = False
    TESTING = False
   

class DevelopmentConfig(Config):
    """Configurations for Development."""
    DEBUG = True


class StagingConfig(Config):
    """Configurations for Staging."""
    DEBUG = True
    
class TestingConfig(Config):
    """Configurations for Testing, with a separate test database."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.getenv('TEST_DATABASE_URL')
    DEBUG = True



app_config = {
    'production': ProductionConfig,
    'development': DevelopmentConfig,
    'staging': StagingConfig,
    'testing': TestingConfig,
}