from langchain.llms.sagemaker_endpoint import LLMContentHandler
from langchain_community.llms import SagemakerEndpoint
from botocore.exceptions import ClientError
from typing import Dict
import boto3
import os
import json


class ContentHandler(LLMContentHandler):

    content_type = 'application/json'
    accepts = 'application/json'

    # Mistral-7B-Instruct requires <s>[INST] boundary tokens in input
    def transform_input(self, prompt: str, model_kwargs: Dict) -> bytes:
        input_string = json.dumps(
            {
                'inputs': f'<s>[INST] {prompt} [/INST]',
                'parameters': {**model_kwargs}
            }
        )
        return input_string.encode('utf-8')
    
    def transform_output(self, output: bytes) -> str:
        response_json = json.loads(output.read().decode('utf-8'))
        answer_split = response_json[0]['generated_text'].split('[/INST] ')
        return answer_split[1]


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