"""
This module sets the configurations for the application
"""
import os


class Config(object):
    """Parent configuration class."""
    DEBUG = False
    CSRF_ENABLED = True
    DATABASE_URL = os.getenv("DATABASE_URL")
    DATABASE_TEST_URL = os.getenv("DATABASE_TEST_URL")


class DevelopmentConfig(Config):
    """Development phase configurations"""
    DEBUG = True
    TESTING = True


class TestingConfig(Config):
    """Testing Configurations."""
    DEBUG = True
    TESTING = True


class ReleaseConfig(Config):
    """Release Configurations."""
    DEBUG = False
    TESTING = False


app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'release': ReleaseConfig,
}
