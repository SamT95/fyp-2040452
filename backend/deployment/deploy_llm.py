from sagemaker.huggingface import HuggingFaceModel, get_huggingface_llm_image_uri
from sagemaker.serverless import ServerlessInferenceConfig
import json
import sys # For sys.stdout during GitHub Actions
import logging

logging.getLogger("sagemaker").setLevel(logging.WARNING)
# Silence 'INFO' logging from huggingface_model.deploy()

def deploy_language_model(role):
    """
    Function to deploy a Hugging Face language model to SageMaker Inference.

    Params:
    - role: SageMaker execution role

    Returns:
    None
    """
    # Hub Model configuration. https://huggingface.co/models
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

    # Set up AWS Serverless Inference Config (https://sagemaker.readthedocs.io/en/stable/overview.html#sagemaker-serverless-inference)

    serverless_config = ServerlessInferenceConfig(
      memory_size_in_mb=6144,
      max_concurrency=2,
    )

    endpoint_name="huggingface-rag-llm-endpoint"

    # deploy model to SageMaker Inference
    predictor = huggingface_model.deploy(
      endpoint_name=endpoint_name,
      serverless_inference_config=serverless_config,
      )
    
    endpoint_name = predictor.endpoint_name
    print(endpoint_name, file=sys.stdout)

# Add ability to execute as script in GitHub Actions
if __name__ == "__main__":
    import os
    role = os.environ.get("SAGEMAKER_EXECUTION_ROLE")
    endpoint_name = deploy_language_model(role)