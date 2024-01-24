from sagemaker.huggingface import HuggingFaceModel, get_huggingface_llm_image_uri
from langchain.llms.sagemaker_endpoint import LLMContentHandler
from langchain.llms import SagemakerEndpoint
from typing import Dict
import boto3
import json

def deploy_language_model(role):
    # Hub Model configuration. https://huggingface.co/models
    print('Beginning model deployment (Mistral ver.)')
    
    # https://huggingface.co/mistralai/Mistral-7B-Instruct-v0.1
    hub = {
    	'HF_MODEL_ID':'mistralai/Mistral-7B-Instruct-v0.1',
    	'SM_NUM_GPUS': json.dumps(1)
    }
    
    huggingface_model = HuggingFaceModel(
    	image_uri=get_huggingface_llm_image_uri("huggingface",version="1.1.0"),
    	env=hub,
    	role=role, 
    )

    # deploy model to SageMaker Inference
    predictor = huggingface_model.deploy(
    	initial_instance_count=1,
    	instance_type="ml.g5.2xlarge",
    	container_startup_health_check_timeout=300,
      )
    
    endpoint_name = predictor.endpoint_name
    print(f'Language model deployed. Endpoint {endpoint_name}')
    print(f'Hub config:\n {hub}')
    return endpoint_name

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

    # If the LLM is not already deployed, uncomment the following line:
    # llm_endpoint_name = deploy_language_model(role)
    # Will be updated to automatically check if it is deployed (i.e. checking if it exists in env or another method)
    llm_endpoint_name = os.environ.get("LLM_ENDPOINT_NAME")
    sagemaker_runtime = boto3.client("sagemaker-runtime")
    content_handler = ContentHandler()
    llm = SagemakerEndpoint(
        endpoint_name=llm_endpoint_name,
        model_kwargs=model_kwargs,
        content_handler=content_handler,
        client=sagemaker_runtime,
    )

    return llm