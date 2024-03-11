import boto3
import json
from botocore.exceptions import ClientError

def fetch_cohere_key():
    """
    This function fetches the Cohere API key from AWS Secrets Manager.
    """

    secret_name = "rag/CohereKeyProd"
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
    # Extract COHERE_API_KEY key from json object
    key = secret["COHERE_API_KEY"]
    return key

def fetch_pinecone_key():
    """
    This function fetches the Pinecone API key from AWS Secrets Manager.
    """

    secret_name = "rag/PineconeKey"
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
    # Extract PINECONE_API_KEY key from json object
    key = secret["PINECONE_API_KEY"]
    return key