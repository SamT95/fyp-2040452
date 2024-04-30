import unittest
from unittest.mock import patch
import json
import os
from scraper.base_scraper import BaseScraper

import requests
from bs4 import BeautifulSoup

class TestBaseScraper(unittest.TestCase):

    @patch('scraper.base_scraper.requests.get')
    def test_init(self, mock_get):
        # Mock the requests.get method
        mock_response = requests.Response()
        mock_response.status_code = 200
        mock_response.url = "http://test.com"
        mock_response._content = b'<html><title>Test Page</title><body><p>Hello, world!</p></body></html>'
        mock_get.return_value = mock_response

        # Call the constructor
        scraper = BaseScraper("http://test.com")

        # Assert that the requests.get method was called twicewith the correct arguments
        mock_get.assert_called_once_with("http://test.com", headers={'User-Agent': 'UP2040452/UoP'}, allow_redirects=True)

        # Assert that the soup attribute was set correctly
        self.assertIsInstance(scraper.soup, BeautifulSoup)
        self.assertEqual(scraper.soup.title.string, "Test Page")

    @patch('scraper.base_scraper.requests.get')
    def test_get_soup(self, mock_get):
        # Create a BaseScraper object
        mock_response = requests.Response()
        mock_response.status_code = 200
        mock_response.url = "http://test.com"
        mock_response._content = b'<html><title>Test Page</title><body><p>Hello, world!</p></body></html>'
        mock_get.return_value = mock_response
        scraper = BaseScraper("http://test.com")

        # Call the get_soup method
        soup = scraper.get_soup()

        # Assert that the method returned the correct value
        self.assertIsInstance(soup, BeautifulSoup)

    @patch('scraper.base_scraper.requests.get')
    def test_get_page(self, mock_get):
        # Create a BaseScraper object
        mock_response = requests.Response()
        mock_response.status_code = 200
        mock_response.url = "http://test.com"
        mock_response._content = b'<html><title>Test Page</title><body><p>Hello, world!</p></body></html>'
        mock_get.return_value = mock_response
        scraper = BaseScraper("http://test.com")

        # Call the get_page method
        page = scraper.get_page()

        # Assert that the method returned the correct value
        self.assertIsInstance(page, requests.Response)

    @patch('scraper.base_scraper.requests.get')
    def test_get_title(self, mock_get):
        # Create a BaseScraper object
        mock_response = requests.Response()
        mock_response.status_code = 200
        mock_response.url = "http://test.com"
        mock_response._content = b'<html><title>Test Page</title><body><p>Hello, world!</p></body></html>'
        mock_get.return_value = mock_response
        scraper = BaseScraper("http://test.com")

        # Call the get_title method
        title = scraper.get_title()

        # Assert that the method returned the correct value
        self.assertEqual(title, "Test Page")

    @patch('scraper.base_scraper.requests.get')
    def test_get_text(self, mock_get):
        # Create a BaseScraper object
        mock_response = requests.Response()
        mock_response.status_code = 200
        mock_response.url = "http://test.com"
        mock_response._content = b'<html><title>Test Page</title><body><p>Hello, world!</p></body></html>'
        mock_get.return_value = mock_response
        scraper = BaseScraper("http://test.com")

        # Call the get_text method
        text = scraper.get_text()

        # Assert that the method returned the correct value
        self.assertEqual(text, "Test PageHello, world!")

    @patch('scraper.base_scraper.requests.get')
    def test_get_links(self, mock_get):
        # Create a BaseScraper object
        mock_response = requests.Response()
        mock_response.status_code = 200
        mock_response.url = "http://test.com"
        mock_response._content = b'<html><a href="http://link1.com">Link 1</a><a href="http://link2.com">Link 2</a></html>'
        mock_get.return_value = mock_response
        scraper = BaseScraper("http://test.com")

        # Call the get_links method
        links = scraper.get_links()

        # Assert that the method returned the correct value
        self.assertEqual(links, ["http://link1.com", "http://link2.com"])

    @patch('scraper.base_scraper.requests.get')
    def test_format_text(self, mock_get):
        # Create a BaseScraper object
        mock_response = requests.Response()
        mock_response.status_code = 200
        mock_response.url = "http://test.com"
        mock_response._content = b'<html><title>Test Page</title><body><p>Hello, world!</p></body></html>'
        mock_get.return_value = mock_response
        scraper = BaseScraper("http://test.com")

        # Call the format_text method
        formatted_text = scraper.format_text("Hello, world!")

        # Assert that the method returned the correct value
        self.assertEqual(formatted_text, "hello, world!")
    

