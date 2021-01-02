import os
import sys

import flask
from flask import Flask
import logging
from logging.handlers import RotatingFileHandler

from .endpoints import link, health
from .config.config import DevelopmentConfig, TestConfig, ProductionConfig


LOG_FILENAME = "logs/app.log"
DOWNLOAD_DIR_NAME = "temp_downloads"
WEBDRIVER_DIR_NAME = "webdrivers"

app = Flask(__name__)

app.register_blueprint(health.health_endpoint)
app.register_blueprint(link.link_endpoint)

log_file = os.path.join(app.root_path, LOG_FILENAME)


if app.env == "DEVELOPMENT":
    # set up the logger
    logging.basicConfig(filename=log_file, level=logging.DEBUG)
    logger = logging.getLogger(__name__)
    # load the environment specific config
    app.config.from_object(DevelopmentConfig)
    from flask_cors import CORS
    CORS(app)
    logger.info("Application started in DEVELOPMENT mode.")
    print("Application started in DEVELOPMENT mode.")
    # make sure the Webdriver is there
    app.config["WEBDRIVER_FILEPATH"] = os.path.join(os.path.abspath(WEBDRIVER_DIR_NAME), app.config["WEBDRIVER_FILENAME"])
    if not os.path.isfile(app.config["WEBDRIVER_FILEPATH"]):
        print("You need a Webdriver specific to your DEVELOPMENT environment with the filepath " + app.config["WEBDRIVER_FILEPATH"])
        sys.exit(1)
    app.config["DOWNLOADS_PARENT_DIRECTORY"] = os.path.join(os.path.curdir, DOWNLOAD_DIR_NAME)

if app.env == "TEST":
    # set up the logger
    logging.basicConfig(filename=log_file, level=logging.DEBUG)
    logger = logging.getLogger(__name__)
    # load the environment specific config
    app.config.from_object(TestConfig)
    logger.info("Application started in TEST mode.")
    print("Application started in TEST mode")
    # make sure the Webdriver is there
    app.config["WEBDRIVER_FILEPATH"] = os.path.join(os.path.join("backend", WEBDRIVER_DIR_NAME), app.config["WEBDRIVER_FILENAME"])
    if not os.path.isfile(app.config["WEBDRIVER_FILEPATH"]):
        print("You need a Webdriver specific to your TEST environment with the filepath " + app.config["WEBDRIVER_FILEPATH"])
        print(os.listdir(os.path.curdir))
        sys.exit(1)
    app.config["DOWNLOADS_PARENT_DIRECTORY"] = os.path.join(os.path.curdir, DOWNLOAD_DIR_NAME)

if app.env == "PRODUCTION":
    # set up the logger
    logging.basicConfig(filename=log_file, level=logging.INFO)
    logger = logging.getLogger(__name__)
    # load the environment specific config
    app.config.from_object(ProductionConfig)
    logger.info("Application started in PRODUCTION mode.")
    print("Application started in PRODUCTION mode")
    # make sure the Webdriver is there
    app.config["WEBDRIVER_FILEPATH"] = os.path.join(os.path.join("backend", WEBDRIVER_DIR_NAME), app.config["WEBDRIVER_FILENAME"])
    if not os.path.isfile(app.config["WEBDRIVER_FILEPATH"]):
        print("You need a Webdriver specific to your PRODUCTION environment with the filepath " + app.config["WEBDRIVER_FILEPATH"])
        sys.exit(1)
    app.config["DOWNLOADS_PARENT_DIRECTORY"] = os.path.join(os.path.curdir, DOWNLOAD_DIR_NAME)

if __name__ == '__main__':
    app.run()
