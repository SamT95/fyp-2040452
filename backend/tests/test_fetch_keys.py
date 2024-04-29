import unittest
import json
from unittest.mock import patch
from rag.common.fetch_keys import fetch_cohere_key, fetch_pinecone_key

class TestFetchKeys(unittest.TestCase):

    @patch("rag.common.fetch_keys.boto3")
    def test_fetch_cohere_key(self, mock_boto3):
        secret = json.dumps({
            "COHERE_API_KEY": "test-key"
        })
        mock_boto3.session.Session().client().get_secret_value.return_value = {
            "SecretString": secret
        }
        key = fetch_cohere_key()
        self.assertEqual(key, "test-key")

    @patch("rag.common.fetch_keys.boto3")
    def test_fetch_pinecone_key(self, mock_boto3):
        secret = json.dumps({
            "PINECONE_API_KEY": "test-key"
        })
        mock_boto3.session.Session().client().get_secret_value.return_value = {
            "SecretString": secret
        }
        key = fetch_pinecone_key()
        self.assertEqual(key, "test-key")

    # Test that an exception is raised when the client fails to fetch the cohere key
    @patch("rag.common.fetch_keys.boto3")
    def test_fetch_cohere_key_exception(self, mock_boto3):
        mock_boto3.session.Session().client().get_secret_value.side_effect = Exception("Failed to fetch secret")
        with self.assertRaises(Exception):
            fetch_cohere_key()

    # Test that an exception is raised when the client fails to fetch the pinecone key
    @patch("rag.common.fetch_keys.boto3")
    def test_fetch_pinecone_key_exception(self, mock_boto3):
        mock_boto3.session.Session().client().get_secret_value.side_effect = Exception("Failed to fetch secret")
        with self.assertRaises(Exception):
            fetch_pinecone_key()
