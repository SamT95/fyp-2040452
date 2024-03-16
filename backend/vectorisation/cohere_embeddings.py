# The code in this file is related to Cohere and generating embeddings using the Cohere API.

import os
import cohere
import boto3
import json
from dotenv import load_dotenv
from botocore.exceptions import ClientError
from langchain_community.embeddings import CohereEmbeddings
from typing import List

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

def batch_embeddings(chunks, batch_size=10):
    """
    This function generates embeddings for the chunks of text using the Cohere API.
    The chunks are passed in as a list of strings.
    The batch size is set to 10 by default, but can be modified.
    """

    cohere_api_key = fetch_cohere_key()
    cohere_client = cohere.Client(api_key=cohere_api_key)
    embeddings = []
    for i in range(0, len(chunks), batch_size):
        print(f"Processing batch {i // batch_size + 1} of {len(chunks) // batch_size + 1}")
        batch = chunks[i:i + batch_size]
        batch_embeddings = cohere_client.embed(
            texts=batch,
            model="embed-english-v3.0",
            input_type="search_document",
        )
        embeddings.extend(batch_embeddings)
    return embeddings
