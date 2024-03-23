from langchain.llms.sagemaker_endpoint import LLMContentHandler
from langchain_community.llms import SagemakerEndpoint
from botocore.exceptions import ClientError
from typing import Dict
import boto3
import os
import json
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class ContentHandler(LLMContentHandler):

    content_type = 'application/json'
    accepts = 'application/json'

    # Mistral-7B-Instruct requires <s>[INST] boundary tokens in input
    def transform_input(self, prompt: str, model_kwargs: Dict) -> bytes:
        """
        Transforms the input for GPT-2.
        Parameters:
        prompt (str): The prompt text to generate text from.
        model_kwargs (dict): Additional model-specific arguments.

        Returns:
        dict: A dictionary with the formatted input for GPT-2.
        """
        input_data = {
            "inputs": prompt,
            **model_kwargs,
        }
        serialized_input = json.dumps(input_data).encode('utf-8')
        return serialized_input
    
    def transform_output(self, output: bytes) -> str:
        response_json = json.loads(output.read().decode('utf-8'))
        # logger.log(logging.INFO, f"Response JSON: {response_json}")
        logger.info(f"Output: {response_json}")
        generated_text = response_json[0]["generated_text"]
        return generated_text


def build_sagemaker_llm_endpoint(role):
    """
    This function builds and returns a SagemakerEndpoint class.
    """

    model_kwargs = {
        "max_new_tokens": 512,
        "top_p": 0.3,
        "temperature": 0.1,
    }

    llm_endpoint_name = "huggingface-rag-llm-endpoint"
    sagemaker_runtime = boto3.client("sagemaker-runtime")
    content_handler = ContentHandler()
    llm = SagemakerEndpoint(
        endpoint_name=llm_endpoint_name,
        model_kwargs=model_kwargs,
        content_handler=content_handler,
        client=sagemaker_runtime,
    )


    return llm