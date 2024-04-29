import unittest
from unittest.mock import patch
import json
import os
from vectorisation.pinecone_store import load_pinecone_index, create_pinecone_index, fetch_pinecone_key

class TestPineconeStore(unittest.TestCase):

    @patch("vectorisation.pinecone_store.fetch_pinecone_key")
    def test_load_pinecone_index(self, mock_fetch_pinecone_key):
        mock_fetch_pinecone_key.return_value = "test-key"
        with patch("vectorisation.pinecone_store.PineconeClient") as mock_pinecone_client:
            mock_pinecone_client.return_value.list_indexes.return_value = [
                {"name": "index1"},
                {"name": "index2"},
                {"name": "index3"}
            ]
            index = load_pinecone_index("index2")
            self.assertIsNotNone(index)

    @patch("vectorisation.pinecone_store.fetch_pinecone_key")
    def test_create_pinecone_index(self, mock_fetch_pinecone_key):
        mock_fetch_pinecone_key.return_value = "test-key"
        with patch("vectorisation.pinecone_store.PineconeClient") as mock_pinecone_client:
            mock_pinecone_client.return_value.list_indexes.return_value = [
                {"name": "index1"},
                {"name": "index3"}
            ]
            index = create_pinecone_index("index2", 1024)
            self.assertIsNotNone(index)

    @patch("vectorisation.pinecone_store.fetch_pinecone_key")
    def test_create_index_already_exists(self, mock_fetch_pinecone_key):
        mock_fetch_pinecone_key.return_value = "test-key"
        with patch("vectorisation.pinecone_store.PineconeClient") as mock_pinecone_client:
            mock_pinecone_client.return_value.list_indexes.return_value = [
                {"name": "index1"},
                {"name": "index2"},
                {"name": "index3"}
            ]
            index = create_pinecone_index("index2", 1024)
            self.assertIsNotNone(index)

    @patch("vectorisation.pinecone_store.boto3")
    def test_fetch_pinecone_key(self, mock_boto3):
        secret = json.dumps({
            "PINECONE_API_KEY": "test-key"
        })
        mock_boto3.session.Session().client().get_secret_value.return_value = {
            "SecretString": secret
        }
        key = fetch_pinecone_key()
        self.assertEqual(key, "test-key")
    

        
        