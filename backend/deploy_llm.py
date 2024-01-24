from sagemaker.huggingface import HuggingFaceModel, get_huggingface_llm_image_uri
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