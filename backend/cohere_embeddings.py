# The code in this file is related to Cohere and generating embeddings using the Cohere API.

import os
import cohere
from dotenv import load_dotenv
from langchain.embeddings import CohereEmbeddings
from typing import List

def fetch_cohere_key():
    """
    This function fetches the Cohere API key from the environment variables.
    """

    load_dotenv()
    return os.getenv("COHERE_API_KEY")

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
        batch_embeddings = co.embed(
            texts=batch,
            model="embed-english-v3.0",
            input_type="search_document",
        )
        embeddings.extend(batch_embeddings)
    return embeddings

class CustomCohereEmbeddings(CohereEmbeddings):
    """
    A custom class which inherits from CohereEmbeddings, a Langchain embeddings class.
    This custom class is required to override the `embed_documents` method of the parent class.
    This is necessary because Cohere Embed v3 requires an 'input_type' parameter, and Langchain does not support this yet.
    """

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """
        This method overrides the `embed_documents` method of the parent class.
        It is necessary because Cohere Embed v3 requires an 'input_type' parameter, and Langchain does not support this yet.
        See https://txt.cohere.com/introducing-embed-v3/ and https://github.com/langchain-ai/langchain/issues/12877
        """

        embeddings = self.client.embed(
            model=self.model,
            texts=texts,
            truncate=self.truncate,
            input_type='search_query'
        ).embeddings
        return [list(map(float, e)) for e in embeddings]
