import os

import flask
from flask import Config


class DevelopmentConfig(Config):
    """
    Development configurations
    """
    DEBUG = True
    WEBDRIVER_FILENAME = "chromedriver_dev"

class TestConfig(Config):
    """
    Test configurations
    """
    DEBUG = True
    # same as the production environment
    WEBDRIVER_FILENAME = "chromedriver"

class ProductionConfig(Config):
    """
    Production configurations
    """
    DEBUG = False
    WEBDRIVER_FILENAME = "chromedriver"
