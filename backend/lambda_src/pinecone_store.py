# The code in this file is related to interactions with the Pinecone vector database.
# Pinecone serverless is being utilised since it requires no configuration of compute or storage resources.
# Serverless indexes scale automatically based on usage. See https://www.pinecone.io/product/

from dotenv import load_dotenv
import os
from pinecone import Pinecone as PineconeClient, ServerlessSpec
from langchain.vectorstores import Pinecone
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
    return secret

def create_pinecone_index(index_name: str, shape: int):
    """
    This function initialises the Pinecone client and creates an index if it doesn't exist.
    The index name is passed as an argument.
    The shape (dimensionality) of the vectors is also passed as an argument.
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

def load_existing_index(index_name: str):
    """
    This function loads an existing index.
    The index name is passed as an argument.
    """

    pinecone_api_key = fetch_pinecone_key()
    pinecone = PineconeClient(api_key=pinecone_api_key)

    pinecone_index_names = [index["name"] for index in pinecone.list_indexes()]

    if index_name not in pinecone_index_names:
        print(f"Index {index_name} does not exist")
        return None
    else:
        print(f"Index {index_name} exists")
    index = pinecone.Index(index_name)
    return index

class CustomPineconeVectorstore(Pinecone):
    """
    A custom class which inherits from Pinecone, a Langchain vectorstore class.
    This custom class is required to override the `custom_similarity_search_by_vector_with_score` method of the parent class.
    This is necessary because the index.query() method utilised in this function requires keyword arguments,
    and the Langchain vectorstore class uses positional arguments by default.
    """

    def custom_similarity_search_by_vector_with_score(self, embedding: List[float], *, k: int = 2, filter: Optional[dict] = None, namespace: Optional[str] = None) -> List[Tuple[Document, float]]:
        """Custom function to correct the arguments supplied to the `query` method of the Pinecone index."""
        if namespace is None:
            namespace = self._namespace
        docs = []
        # Embedding requires keyword arguments (i.e. `vector=embedding`, not just `embedding`)
        # If run without using keyword arguments, an error is raised, hence the need for this custom function override.
        results = self._index.query(
            vector=embedding,
            top_k=k,
            include_metadata=True,
            namespace=namespace,
            filter=filter,
        )
        for res in results["matches"]:
            metadata = res["metadata"]
            if self._text_key in metadata:
                text = metadata.pop(self._text_key)
                score = res["score"]
                docs.append((Document(page_content=text, metadata=metadata), score))
            else:
                print(
                    f"Found document with no `{self._text_key}` key. Skipping."
                )
        return docs
