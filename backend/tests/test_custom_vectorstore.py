import unittest
from unittest.mock import patch
import json
from rag.common.custom_vectorstore import CustomPineconeVectorstore, load_existing_index

class TestCustomVectorStore(unittest.TestCase):

    @patch("rag.common.custom_vectorstore.fetch_pinecone_key")
    def test_load_existing_index(self, mock_fetch_pinecone_key):
        mock_fetch_pinecone_key.return_value = "test-key"
        with patch("rag.common.custom_vectorstore.PineconeClient") as mock_pinecone_client:
            mock_pinecone_client.return_value.list_indexes.return_value = [
                {"name": "index1"},
                {"name": "index2"},
                {"name": "index3"}
            ]
            index = load_existing_index("index2")
            self.assertIsNotNone(index)

    @patch("rag.common.custom_vectorstore.fetch_pinecone_key")
    def test_load_existing_index_not_found(self, mock_fetch_pinecone_key):
        mock_fetch_pinecone_key.return_value = "test-key"
        with patch("rag.common.custom_vectorstore.PineconeClient") as mock_pinecone_client:
            mock_pinecone_client.return_value.list_indexes.return_value = [
                {"name": "index1"},
                {"name": "index3"}
            ]
            index = load_existing_index("index2")
            self.assertIsNone(index)

    @patch("rag.common.custom_vectorstore.fetch_pinecone_key")
    def test_load_existing_index_no_indexes(self, mock_fetch_pinecone_key):
        mock_fetch_pinecone_key.return_value = "test-key"
        with patch("rag.common.custom_vectorstore.PineconeClient") as mock_pinecone_client:
            mock_pinecone_client.return_value.list_indexes.return_value = []
            index = load_existing_index("index2")
            self.assertIsNone(index)

