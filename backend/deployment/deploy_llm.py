from sagemaker.huggingface import HuggingFaceModel, get_huggingface_llm_image_uri
from sagemaker.serverless import ServerlessInferenceConfig
import json
import sys # For sys.stdout during GitHub Actions
import logging
import os

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
        "HF_MODEL_ID": "mistralai/Mistral-7B-Instruct-v0.1",
        "SM_NUM_GPUS": json.dumps(1),
        "HUGGING_FACE_HUB_TOKEN": os.environ.get("HUGGING_FACE_HUB_TOKEN"), 
    }
    
    huggingface_model = HuggingFaceModel(
    	image_uri=get_huggingface_llm_image_uri("huggingface",version="1.4.2"),
    	env=hub,
    	role=role, 
    )

    endpoint_name="huggingface-rag-llm-endpoint"

    # deploy model to SageMaker Inference
    predictor = huggingface_model.deploy(
        initial_instance_count=1,
        instance_type="ml.g5.2xlarge",
        endpoint_name=endpoint_name,
        container_startup_health_check_timeout=300,
    )
    
    endpoint_name = predictor.endpoint_name
    print(endpoint_name, file=sys.stdout)

# Add ability to execute as script in GitHub Actions
if __name__ == "__main__":
    import os
    role = os.environ.get("SAGEMAKER_EXECUTION_ROLE")
    endpoint_name = deploy_language_model(role)