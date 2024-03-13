from langchain_community.vectorstores import Pinecone
from typing import List, Tuple, Optional
from langchain.docstore.document import Document
from .fetch_keys import fetch_pinecone_key
from pinecone import Pinecone as PineconeClient

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