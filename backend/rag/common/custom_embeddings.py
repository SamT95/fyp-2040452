from langchain_community.embeddings import CohereEmbeddings
from typing import List

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