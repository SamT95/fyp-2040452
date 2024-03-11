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
    

def fetch_endpoint_name():
    """
    This function fetches the endpoint name from AWS Secrets Manager.
    """

    secret_name = "rag/LLMEndpointName"
    region_name = "eu-west-1"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        raise e
    
    secret = get_secret_value_response['SecretString']
    secret = json.loads(secret)
    # Extract LLM_ENDPOINT_NAME key from json object
    endpoint_name = secret["LLM_ENDPOINT_NAME"]
    return endpoint_name

def build_sagemaker_llm_endpoint(role):
    """
    This function builds and returns a SagemakerEndpoint class.
    """

    model_kwargs = {
        "max_new_tokens": 512,
        "top_p": 0.3,
        "temperature": 0.1,
    }

    llm_endpoint_name = fetch_endpoint_name()
    sagemaker_runtime = boto3.client("sagemaker-runtime")
    content_handler = ContentHandler()
    llm = SagemakerEndpoint(
        endpoint_name=llm_endpoint_name,
        model_kwargs=model_kwargs,
        content_handler=content_handler,
        client=sagemaker_runtime,
        streaming=True,
    )

    return llm