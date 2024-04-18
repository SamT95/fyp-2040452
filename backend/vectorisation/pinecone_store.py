# The code in this file is related to interactions with the Pinecone vector database.
# Pinecone serverless is being utilised since it requires no configuration of compute or storage resources.
# Serverless indexes scale automatically based on usage. See https://www.pinecone.io/product/

import os
import json
import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv
from pinecone import Pinecone as PineconeClient, ServerlessSpec
from langchain_community.vectorstores import Pinecone
from typing import List, Tuple, Optional
from langchain.docstore.document import Document

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

def create_pinecone_index(index_name: str, shape: int):
    """
    This function initialises the Pinecone client and creates an index if it doesn't exist.
    The index name is passed as an argument.
    The shape (dimensionality) of the vectors is also passed as an argument.

    Parameters:
    index_name (str): Name of the index to create
    shape (int): Dimensionality of the vectors

    Returns:
    pinecone.Index: Pinecone index object
    """

    # The shape is passed in as an argument, though it could be hardcoded.
    # Cohere embeddings have 1024 dimensions.

    pinecone_api_key = fetch_pinecone_key()
    pinecone = PineconeClient(api_key=pinecone_api_key)
    if index_name not in pinecone.list_indexes():
        pinecone.create_index(
            name=index_name,
            dimension=shape,
            metric="cosine",
            spec=ServerlessSpec(
                cloud="aws",
                region="us-west-2",
            )
        )
        print(f"Created index {index_name}")
    else:
        print(f"Index {index_name} already exists")
    index = pinecone.Index(index_name)
    return index

def load_pinecone_index(index_name: str):
    """
    This function initialises the Pinecone client and loads an existing index (if it exists).
    If the index does not exist, it is created.

    Parameters:
    index_name (str): Name of the index to load (or create)

    Returns:
    pinecone.Index: Pinecone index object
    """
    pinecone_api_key = fetch_pinecone_key()
    pinecone = PineconeClient(api_key=pinecone_api_key)
    if index_name not in pinecone.list_indexes():
        print(f"Index {index_name} does not exist. Creating...")
        index = create_pinecone_index(index_name, 1024)
    else:
        print(f"Loading index {index_name}")
        index = pinecone.Index(index_name)
    return index