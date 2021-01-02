import os
from uuid import uuid4
import shutil
from time import time
import logging

import requests
import flask
import selenium
from selenium.common.exceptions import NoSuchElementException, TimeoutException, InvalidArgumentException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# DOWNLOADS_PARENT_DIRECTORY = os.path.join(flask.current_app.root_path, "temp_downloads")

link_endpoint = flask.Blueprint('link_endpoint', __name__)

logger = logging.getLogger(__name__)

def get_downloaded_filenames(directory):
    """Retrieves a list of filenames.

    Retrieves a list of filenames for files downloaded
    to a specific directory.

    Args:
      directory:
        Location of files.

    Returns:
      A list of string filenames.

      ["file1.txt", "file2.png"]
    """

    result = []
    # check if the directory exists
    # if os.path.isdir(os.path.abspath(directory)) is True:
    if os.path.isdir(directory) is True:
        # get filenames for downloads
        # result = os.listdir(os.path.abspath(directory))
        result = os.listdir(directory)
    else:
        # log an error if the directory does not exist
        logger.info("Attempted to list file in temp download directory that did not exist: " + directory)

    return result

def get_iframe_urls(driver):
    """Retrieves a list of iframe URLs.

    Retrieves a list of Iframe URLs for a webpage from
    a given URL, if the Iframe has a URL.

    Args:
      driver:
        Webdriver instance which was used to perform 
        the RESTful GET request on the target URL.

    Returns:
      A list of string Iframe URLs.

      ["https://c832e2658ac4c552a1332a415b695ac8.safeframe.googlesyndication.com/safeframe/1-0-37/html/container.html", 
      "https://c832e2658ac4c552a1332a415b695ac8.safeframe.googlesyndication.com/safeframe/1-0-37/html/container.html",
      "https://c832e2658ac4c552a1332a415b695ac8.safeframe.googlesyndication.com/safeframe/1-0-37/html/container.html"]
    """
    
    result = []
    try:
        # get Iframes within a URL's hypertext
        iframes = driver.find_elements_by_tag_name('iframe')
        for iframe in iframes:
            # if an Iframe has a URL, append that to the result
            if iframe.get_property('src'):
                result.append(iframe.get_property('src'))
    # the hypertext from a URL may not have Iframes at all
    except NoSuchElementException:
        pass

    return result

def get_urls(driver, url):
    """Retrieves a list of URLs.

    Retrieves a list of URLs visited during any number
    of redirects before arriving at the landing page. This
    may not include URLs redirected to due to parsing the
    hypertext itself.
    https://developer.mozilla.org/en-US/docs/Web/HTTP/Redirections#Alternative_way_of_specifying_redirections

    Args:
        driver:
          Webdriver instance which was used to perform 
          the RESTful GET request on the target URL.
        url:
          The target URL.

    Returns:
      Two lists of string URLs. The first list contains a single element,
      the landing page's URL. The second list contains all URLs redirected to.

      ["https://www.facebook.com/], ["http://facebook.com", "https://www.facebook.com/"]

      The first list should contain a single URL. The second list includes the original URL visited.
    """

    redirect_result = []
    landing_result = []

    response = requests.get(url, allow_redirects=True)
    history = response.history
    for h in history:
      redirect_result.append(h.url)
    redirect_result.append(driver.current_url)
    landing_result.append(driver.current_url)
    
    return landing_result, redirect_result

# aggregate metrics from various metric gathering operations
def get_metrics(driver, url, temp_download_directory):
    # this runs as the page loads
    landing_url, redirect_urls = get_urls(driver=driver, url=url)
    # this runs on the final landing page
    iframe_urls = get_iframe_urls(driver=driver)
    # this runs last to see if anything was downloaded along the way
    download_filenames = get_downloaded_filenames(directory=temp_download_directory)

    return landing_url, redirect_urls, iframe_urls, download_filenames

def teardown_driver(driver):
    driver.close()

def initialize_driver(driver, url):
    """Initializes Webdriver instance with URL.

    Using the instance of the Webdriver, the URL is accessed
    via a RESTful GET request.

    Args:
        driver:
          Webdriver instance which was used to perform 
          the RESTful GET request on the target URL.
        url:
          The target URL.

    Raises:
        InvalidAttributeError:
          This occurs if the URL being accessed is malformed.
    """
    
    # use the Webdriver to RESTful GET the contents of the URL
    #  and begin parsing/running the hypertext
    driver.get(url=url)

def teardown_downloads(directory):
    """Removes a directory and its contents.

    Removes a directory and its contents from the 
    file system.

    Args:
      directory:
        Location of files.
    """
    
    # check if a directory exists
    # if os.path.isdir(os.path.abspath(directory)) is True:
    if os.path.isdir(directory) is True:
        # delete that directory and its contents
        # shutil.rmtree(os.path.abspath(directory))
        shutil.rmtree(directory)
    else:
        # log an error if the directory does not exist
        logger.info("Attempted to remove temp download directory that did not exist: " + directory)

def initialize_downloads(directory):
    """Initializes directory.

    Creates a directory on the file system.

    Args:
        directory:
            UUID Version 4 string, that is the name
            of the directory.
          
    Raises:
        FileExistsError:
          This occurs if the directory already exists (is not unique
          for some reason).
    """

    os.makedirs(directory)

def setup():
    """Instantiates a Webdriver and generates a directory filename.

    Instantiates a Webdriver and generates a unique directory filename.

    Returns:
      A Webdriver instance and a unique UUID Version 4 string which is used for creating
      a directory.
    """

    # set global preferences for WebDriver
    options = selenium.webdriver.ChromeOptions()
    options.add_argument(argument='-headless')
    options.add_argument(argument='--no-sandbox')
    options.add_argument(argument="--window-size=1920,1080")

    # create a UUID Version 4 unique directory name to store files downloaded by the Webdriver
    temp_download_directory = os.path.join(flask.current_app.config['DOWNLOADS_PARENT_DIRECTORY'], str(uuid4()))
    
    # set local preferences for Webdriver
    # prefs = {"download.default_directory": os.path.abspath(temp_download_directory)}
    # prefs = {"download.default_directory": os.path.join(flask.current_app.root_path, temp_download_directory)}
    prefs = {"download.default_directory": temp_download_directory}
    options.add_experimental_option("prefs", prefs)
    
    # create an instance of the Webdriver
    # driver = selenium.webdriver.Chrome(executable_path=os.path.abspath(flask.current_app.config["WEBDRIVER_FILENAME"]), options=options)
    driver = selenium.webdriver.Chrome(executable_path=flask.current_app.config["WEBDRIVER_FILEPATH"], options=options)

    return driver, temp_download_directory

@link_endpoint.route("/api/link", methods=['POST'])
def link():
    """Returns a variety of metrics about a URL.

    Emulates a web browser via a Webdriver and
    accesses the given URL. Then various operations
    are performed in order to extract information
    about the web page served by the target URL.

    Args:
      url:
        The target url.

    Returns:
      A json object, meant to be consumed by the frontend,
      containing metrics about the
      web page served by the target URL.
    """

    # retrieve JSON object containing URL from frontend call
    params = flask.request.get_json(force=True)
    url = params['url']

    # instantiate a driver and generate a directory name for storing files
    driver, temp_download_directory = setup()
    try:
        # begin tracking elapsed time
        begin = time()
        # create the directory for storing files
        initialize_downloads(directory=temp_download_directory)
        # use the Webdriver to access the URL's hypertext
        initialize_driver(driver=driver, url=url)
        # retrieve metrics from Webdriver and directory
        landing_url, redirect_urls, iframe_urls, download_filenames = get_metrics(driver=driver, url=url, temp_download_directory=temp_download_directory)
        # end tracking elapsed time
        elapsed_time = time() - begin
        # generate response to frontend
        response = {"status": 0, "data": [{"category": "Elapsed Time", "content": ["{:.2f} seconds".format(elapsed_time),]},
                                {"category": "Visited URLs", "content": redirect_urls},
                                {"category": "Landing URL", "content": landing_url},
                                {"category": "Landing Page Iframe URLs", "content": iframe_urls},
                                {"category": "Files Downloaded", "content": download_filenames}]
        }
    except InvalidArgumentException:
        # this error occurs when the Webdriver tries to RESTful GET a malformed URL
        response = {"status": 1, "message": "Invalid URL"}
    except FileExistsError:
        # this error occurs when there is an attempt to create a directory that already exists
        logger.info("Duplicate directory exists: " + temp_download_directory)
        response = {"status": 1, "message": "There was an internal error, please try again."}
    finally:
        # make sure to close the Webdriver and remove the directory, and its contents,
        #  before the program ends
        teardown_driver(driver=driver)
        teardown_downloads(directory=temp_download_directory)

    return flask.jsonify(response)
