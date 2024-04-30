import unittest
from unittest.mock import patch, MagicMock
import json
import os
import requests
from scraper.cve_scraper import CveScraper

class TestCveScraper(unittest.TestCase):

    def setUp(self):
        patcher = patch('scraper.cve_scraper.requests.get')
        self.addCleanup(patcher.stop)
        self.mock_get = patcher.start()

    

    def test_get_latest_cve_zip(self):
        # Mock the requests.get method
        mock_response = requests.Response()
        mock_response.status_code = 200
        mock_response.url = "http://test.com"
        mock_response._content = b'{"assets":[{"name":"delta_CVEs.zip"}]}'
        self.mock_get.return_value = mock_response

        # Call the get_latest_cve_zip method
        scraper = CveScraper()
        latest_zip = scraper.get_latest_cve_zip()

        # Assert that the method returned the correct value
        self.assertEqual(latest_zip, {"name": "delta_CVEs.zip"})

    @patch('scraper.cve_scraper.requests.get')
    @patch('scraper.cve_scraper.zipfile.ZipFile')
    def test_process_cve_zip(self, mock_zipfile, mock_get_zip):
        # Mock the requests.get method
        mock_response = requests.Response()
        mock_response.status_code = 200
        mock_response.url = "http://test.com"
        mock_response._content = b'{"assets":[{"name":"delta_CVEs.zip"}]}'
        self.mock_get.return_value = mock_response

        # Mock the api request in the process_cve_zip method
        mock_zip_response = requests.Response()
        mock_zip_response.status_code = 200
        mock_zip_response.url = "http://test.com/delta_CVEs.zip"
        mock_zip_response._content = b'contents'
        mock_get_zip.return_value = mock_zip_response

        # Mock the zipfile handling
        mock_zip = MagicMock()
        mock_zipfile.return_value.__enter__.return_value = mock_zip
        mock_zip.infolist.return_value = [MagicMock(filename="file1.json")]
        mock_file = MagicMock()
        mock_file.read.return_value = b'{"key": "value"}'
        mock_zip.open.return_value.__enter__.return_value = mock_file


        # Call the process_cve_zip method
        scraper = CveScraper()
        json_data = scraper.process_cve_zip("http://test.com/delta_CVEs.zip")

        # Assert that the method returned the correct value
        self.assertEqual(json_data, [{"key": "value"}])

    def test_process_json_files(self):
        # Create a mock json file
        json_file = [
            {
                "cveMetadata": {
                    "cveId": "test-cve-1",
                    "datePublished": "test-date"
                },
                "containers": {
                    "cna": {
                        "affected": [
                            {
                                "product": "test-product-1"
                            }
                        ],
                        "descriptions": [
                            {
                                "value": "test-description"
                            }
                        ],
                        "references": [
                            {
                                "url": "test-url-1"
                            },
                            {
                                "url": "test-url-2"
                            }
                        ]
                    }
                }
            }
        ]

        # Define the expected formatted cve data
        formatted_cve_data = {
            "cve_id": "test-cve-1",
            "published_date": "test-date",
            "affected_products": "test-product-1",
            "description": "test-description",
            "references": ["test-url-1", "test-url-2"]
        }

        # Mock the requests.get method
        mock_response = requests.Response()
        mock_response.status_code = 200
        mock_response.url = "http://test.com"
        mock_response._content = b'{"assets":[{"name":"delta_CVEs.zip"}]}'
        self.mock_get.return_value = mock_response

        # Call the process_json_files method
        scraper = CveScraper()
        result = scraper.process_json_files(json_file)

        # Assert that the method returned the correct value
        self.assertEqual(result, [formatted_cve_data])

    def test_process_json_files_no_data(self):
        # Create a mock json file with no data
        json_file = [{}]

        # Mock the requests.get method
        mock_response = requests.Response()
        mock_response.status_code = 200
        mock_response.url = "http://test.com"
        mock_response._content = b'{"assets":[{"name":"delta_CVEs.zip"}]}'
        self.mock_get.return_value = mock_response

        # Call the process_json_files method
        scraper = CveScraper()
        result = scraper.process_json_files(json_file)

        # Assert that the method returned the correct value
        self.assertEqual(result, [{"cve_id": "", "published_date": "", "affected_products": "N/A", "description": "N/A", "references": []}])        



