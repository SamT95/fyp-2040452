import unittest
from unittest.mock import patch
import json
import os
from rag.build_llm_endpoint import build_sagemaker_llm_endpoint, ContentHandler

class TestBuildLLMEndpoint(unittest.TestCase):

    def test_transform_input(self):
        content_handler = ContentHandler()
        model_kwargs = {
            "max_new_tokens": 256,
            "top_p": 0.3,
            "temperature": 0.1,
        }
        prompt = "What is the best way to secure my computer?"
        expected_input = json.dumps(
            {
                'inputs': f'<s>[INST] {prompt} [/INST]',
                'parameters': {**model_kwargs}
            }
        ).encode('utf-8')
        self.assertEqual(content_handler.transform_input(prompt, model_kwargs), expected_input)

    def test_transform_output(self):
        content_handler = ContentHandler()
        output = json.dumps([{"generated_text": "<s>Here is the answer[/INST] correct response"}]).encode('utf-8')
        self.assertEqual(content_handler.transform_output(output), "correct response")

    @patch("rag.build_llm_endpoint.boto3")
    def test_build_sagemaker_llm_endpoint(self, mock_boto3):
        os.environ["SAGEMAKER_EXECUTION_ROLE"] = "test-role"
        llm = build_sagemaker_llm_endpoint("test-role")
        self.assertEqual(llm.endpoint_name, "huggingface-rag-llm-endpoint")
        self.assertEqual(llm.model_kwargs, {
            "max_new_tokens": 256,
            "top_p": 0.3,
            "temperature": 0.1,
        })
        self.assertIsInstance(llm.content_handler, ContentHandler)
        self.assertEqual(llm.client, mock_boto3.client.return_value)
        self.assertEqual(llm.client, mock_boto3.client.return_value)