import unittest
from unittest.mock import patch
import json
import os
from chat_history.lambda_handler import lambda_handler

class TestChatHistory(unittest.TestCase):

    def test_missing_query_string_parameters(self):
        os.environ["TABLE_NAME"] = "test-table"
        event = {}
        response = lambda_handler(event, None)
        self.assertEqual(response["statusCode"], 400)
        self.assertEqual(json.loads(response["body"]), {"error": "User ID or conversation ID not found in query string parameters"})

    def test_missing_user_id(self):
        os.environ["TABLE_NAME"] = "test-table"
        event = {
            "queryStringParameters": {
                "conversation_id": "conversation1"
            }
        }
        response = lambda_handler(event, None)
        self.assertEqual(response["statusCode"], 400)
        self.assertEqual(json.loads(response["body"]), {"error": "User ID or conversation ID not found in query string parameters"})

    def test_missing_conversation_id(self):
        os.environ["TABLE_NAME"] = "test-table"
        event = {
            "queryStringParameters": {
                "user_id": "user1"
            }
        }
        response = lambda_handler(event, None)
        self.assertEqual(response["statusCode"], 400)
        self.assertEqual(json.loads(response["body"]), {"error": "User ID or conversation ID not found in query string parameters"})

    @patch("chat_history.lambda_handler.boto3")
    def test_chat_history(self, mock_boto3):
        os.environ["TABLE_NAME"] = "test-table"
        event = {
            "queryStringParameters": {
                "user_id": "user1",
                "conversation_id": "conversation1"
            }
        }
        table = mock_boto3.resource().Table()
        table.query.return_value = {
            "Items": [
                {
                    "user_id": "user1",
                    "conversation_id_timestamp": "conversation1_2020-01-01T00:00:00",
                    "message": "Hello"
                },
                {
                    "user_id": "user1",
                    "conversation_id_timestamp": "conversation1_2020-01-01T00:01:00",
                    "message": "Hi"
                }
            ]
        }
        response = lambda_handler(event, None)
        self.assertEqual(response["statusCode"], 200)
        self.assertEqual(json.loads(response["body"]), {
            "chat_history": [
                {
                    "user_id": "user1",
                    "conversation_id_timestamp": "conversation1_2020-01-01T00:00:00",
                    "message": "Hello"
                },
                {
                    "user_id": "user1",
                    "conversation_id_timestamp": "conversation1_2020-01-01T00:01:00",
                    "message": "Hi"
                }
            ]
        })

    @patch("chat_history.lambda_handler.boto3")
    def test_no_items(self, mock_boto3):
        os.environ["TABLE_NAME"] = "test-table"
        event = {
            "queryStringParameters": {
                "user_id": "user1",
                "conversation_id": "conversation1"
            }
        }
        table = mock_boto3.resource().Table()
        table.query.return_value = {}
        response = lambda_handler(event, None)
        self.assertEqual(response["statusCode"], 200)
        self.assertEqual(json.loads(response["body"]), {
            "chat_history": []
        })

