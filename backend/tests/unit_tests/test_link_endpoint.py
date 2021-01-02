import os
import shutil
from uuid import uuid4

import flask
import selenium
from selenium.common.exceptions import InvalidArgumentException

from backend.endpoints.link import get_downloaded_filenames, get_iframe_urls, teardown_downloads, get_urls, get_metrics, setup, link
import backend


class TestLink:
    def test_teardown_downloads_directory_exists(self, mocker):
        temp_download_directory = mocker.MagicMock()
        mocker.patch('shutil.rmtree')
        mocker.patch('os.path.isdir', return_value=True)

        teardown_downloads(directory=temp_download_directory)

        shutil.rmtree.assert_called_once()

    def test_teardown_downloads_directory_does_not_exist(self, mocker):
        temp_download_directory = mocker.MagicMock()
        mocker.patch('backend.endpoints.link.logger.info')
        mocker.patch('shutil.rmtree')
        mocker.patch('os.path.isdir', return_value=False)

        teardown_downloads(directory=temp_download_directory)

        shutil.rmtree.assert_not_called()
        backend.endpoints.link.logger.info.assert_called_once()

    def test_get_downloaded_filenames_directory_exists(self, mocker):
        download_filenames = ["one", "two", "three"]
        temp_download_directory = mocker.MagicMock()
        mocker.patch('os.listdir', return_value=download_filenames)
        mocker.patch('os.path.isdir', return_value=True)
        
        result = get_downloaded_filenames(directory=temp_download_directory)
        
        assert result == download_filenames

    def test_get_downloaded_filenames_directory_does_not_exist(self, mocker):
        temp_download_directory = mocker.MagicMock()
        mocker.patch('backend.endpoints.link.logger.info')
        mocker.patch('os.listdir')
        mocker.patch('os.path.isdir', return_value=False)
        
        result = get_downloaded_filenames(directory=temp_download_directory)
        
        os.listdir.assert_not_called()
        backend.endpoints.link.logger.info.assert_called_once()
        assert result == []

    def test_get_iframe_urls(self, mocker):
        mock_iframe_url = "mock_iframe_url"
        mock_iframe = mocker.MagicMock()
        mock_iframe.get_property.return_value = mock_iframe_url
        iframe_urls = [mock_iframe]
        mock_driver = mocker.patch("selenium.webdriver.Chrome")
        mock_driver.find_elements_by_tag_name.return_value = iframe_urls

        result = get_iframe_urls(driver=mock_driver)

        assert result == [mock_iframe_url]
        
    def test_get_urls(self, mocker):
        mock_url = "mock_url"
        mock_redirect_url = "mock_redirect_url"
        mock_current_url = "mock_current_url"
        mock_url_response = mocker.MagicMock()
        mock_url_response.url = mock_url
        mock_redirect_response = mocker.MagicMock()
        mock_redirect_response.url = mock_redirect_url
        mock_history = mocker.MagicMock()
        mock_history.history = [mock_url_response, mock_redirect_response]
        mocker.patch("requests.get", return_value=mock_history)
        
        mock_driver = mocker.patch("selenium.webdriver.Chrome")
        mock_driver.current_url = mock_current_url
        
        landing_result, redirect_result = get_urls(driver=mock_driver, url=mock_url)

        assert landing_result == [mock_current_url]
        assert redirect_result == [mock_url, mock_redirect_url, mock_current_url]

    def test_get_metrics(self, mocker):
        urls = (["url0", "url1"], ["url2"])
        iframe_urls = ["iframe_url0", "iframe_url1"]
        download_filenames = ["filename0", "filename1"]
        mocker.patch("backend.endpoints.link.get_urls", return_value=urls)
        mocker.patch("backend.endpoints.link.get_iframe_urls", return_value=iframe_urls)
        mocker.patch("backend.endpoints.link.get_downloaded_filenames", return_value=download_filenames)

        driver = mocker.MagicMock()
        url = mocker.MagicMock()
        temp_download_directory = mocker.MagicMock()
        landing_url, redirect_urls, iframe_urls, download_filenames = get_metrics(driver=driver, url=url, temp_download_directory=temp_download_directory)

        assert ((landing_url, redirect_urls), iframe_urls, download_filenames) == (urls, iframe_urls, download_filenames)

    def test_setup(self, mocker):
        mock_driver = mocker.MagicMock()
        mocker.patch("selenium.webdriver.ChromeOptions")
        mocker.patch("os.mkdir")
        mocker.patch("selenium.webdriver.Chrome", return_value=mock_driver)

        with backend.app.app.app_context():
            driver, temp_download_directory = setup()

        assert driver == mock_driver
        assert isinstance(temp_download_directory, str)
