from rag.lambda_handler import lambda_handler
import unittest
from unittest.mock import patch
import json
import os

class TestLambdaHandler(unittest.TestCase):

    def test_missing_query_string_parameters(self):
        os.environ["TABLE_NAME"] = "test-table"
        event = {}
        response = lambda_handler(event, None)
        self.assertEqual(response["statusCode"], 400)
        self.assertEqual(json.loads(response["body"]), {"error": "Parameters missing from request body"})

    def test_missing_query(self):
        os.environ["TABLE_NAME"] = "test-table"
        event = {
            "body": json.dumps({
                "user_id": "user1",
                "conversation_id": "conversation1"
            })
        }
        response = lambda_handler(event, None)
        self.assertEqual(response["statusCode"], 400)
        self.assertEqual(json.loads(response["body"]), {"error": "Parameters missing from request body"})

    def test_missing_user_id(self):
        os.environ["TABLE_NAME"] = "test-table"
        event = {
            "body": json.dumps({
                "query": "Hello",
                "conversation_id": "conversation1"
            })
        }
        response = lambda_handler(event, None)
        self.assertEqual(response["statusCode"], 400)
        self.assertEqual(json.loads(response["body"]), {"error": "Parameters missing from request body"})

    # def test_missing_conversation_id(self):
    #     os.environ["TABLE_NAME"] = "test-table"
    #     event = {
    #         "body": json.dumps({
    #             "query": "Hello",
    #             "user_id": "user1"
    #         })
    #     }
    #     response = lambda_handler(event, None)
    #     self.assertEqual(response["statusCode"], 400)
    #     self.assertEqual(json.loads(response["body"]), {"error": "Query parameter not found in request body"})

    @patch("rag.lambda_handler.create_qa_chain")
    @patch("rag.lambda_handler.DynamoDBChatMessageHistory")
    def test_lambda_handler(self, mock_DynamoDBChatMessageHistory, mock_create_qa_chain):
        os.environ["TABLE_NAME"] = "test-table"
        event = {
            "body": json.dumps({
                "query": "Hello",
                "user_id": "user1",
                "conversation_id": "conversation1"
            })
        }
        chain = mock_create_qa_chain()
        chat_history = mock_DynamoDBChatMessageHistory()
        chat_history.__str__.return_value = "Chat history"
        chat_history.__getitem__.return_value = "Conversation ID"
        chain.invoke.return_value = {
            "answer": "Hi",
            "context": "Context"
        }
        response = lambda_handler(event, None)
        self.assertEqual(response["statusCode"], 200)
        self.assertEqual(json.loads(response["body"]), {
            "result": "Hi",
            "source_documents": "Context"
        })