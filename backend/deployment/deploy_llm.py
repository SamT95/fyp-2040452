from sagemaker.huggingface import HuggingFaceModel, get_huggingface_llm_image_uri
import json
import sys # For sys.stdout during GitHub Actions
import logging

logging.getLogger("sagemaker").setLevel(logging.WARNING)
# Silence 'INFO' logging from huggingface_model.deploy()

def deploy_language_model(role):
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

    # deploy model to SageMaker Inference
    predictor = huggingface_model.deploy(
    	initial_instance_count=1,
    	instance_type="ml.g5.2xlarge",
    	container_startup_health_check_timeout=300,
      )
    
    endpoint_name = predictor.endpoint_name
    print(endpoint_name, file=sys.stdout)

# Add ability to execute as script in GitHub Actions
if __name__ == "__main__":
    import os
    role = os.environ.get("SAGEMAKER_EXECUTION_ROLE")
    endpoint_name = deploy_language_model(role)