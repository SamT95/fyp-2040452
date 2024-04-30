import unittest
from unittest.mock import patch, MagicMock
from rag.common.custom_embeddings import CustomCohereEmbeddings
from langchain_community.embeddings import CohereEmbeddings


class TestCustomEmbeddings(unittest.TestCase):

    def setUp(self):
        self.embeddings_instance = CustomCohereEmbeddings(cohere_api_key='fake_key', model='fake_model')

    @patch("rag.common.custom_embeddings.CohereEmbeddings")
    def test_embed_documents(self, mock_cohere_embeddings):
        # Mock the necessary dependencies
        mock_cohere_embeddings.return_value = MagicMock()
        self.embeddings_instance.client = MagicMock()
        self.embeddings_instance.model = "model"
        self.embeddings_instance.truncate = "truncate"
        self.embeddings_instance.client.embed.return_value = MagicMock()
        self.embeddings_instance.client.embed.return_value.embeddings = [[0.1, 0.2, 0.3], [0.4, 0.5, 0.6]]

        # Call the function under test
        result = self.embeddings_instance.embed_documents(["text1", "text2"])

        # Assert that the necessary dependencies were called with the correct arguments
        self.embeddings_instance.client.embed.assert_called_once_with(model="model", texts=["text1", "text2"],
                                                                       truncate="truncate", input_type='search_query')

        # Assert that the function returned the expected result
        self.assertEqual(result, [[0.1, 0.2, 0.3], [0.4, 0.5, 0.6]])

