import openai
from qdrant_client import QdrantClient
from typing import List, Dict


class QdrantRetriever:
    """
    Class for retrieving information from Qdrant.
    """
    def __init__(self, collection_name: str, qdrant_url: str, k: int = 3):
        """
        Initialize the QdrantRetriever class for working with Qdrant and OpenAI.

        :param collection_name: Name of the collection in Qdrant to search in.
        :param qdrant_url: URL of Qdrant instance (default is localhost).
        :param k: Number of results to return.
        """
        self.collection_name = collection_name
        self.client = QdrantClient(url=qdrant_url)  # Connect to Qdrant
        self.k = k  # Number of search results to return

    def get_openai_embedding(self, query: str, model: str = "text-embedding-3-small") -> list:
        """
        Generate an embedding for the input query using OpenAI.

        :param query: Text query to generate the embedding.
        :param model: OpenAI model to use for embeddings (default: "text-embedding-3-small").
        :return: Embedding vector for the query.
        """
        response = openai.embeddings.create(input=[query], model=model)

        embedding = response.data[0].embedding
        return embedding    

    def search_medical_guidelines(self, query: str) -> List[Dict]:
        """
        Perform a search in Qdrant using embedding and optional metadata filters.

        :param query: Text query to search in the collection.
        :return: List of search results with relevant metadata.
        """
        query_vector = self.get_openai_embedding(query)

        search_results = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_vector,
            limit=self.k,
            with_payload=True,
        )

        # Format results to return as a list of dictionaries
        results = []
        for result in search_results:
            result_data = {
                "document": result.payload.get("title"),
                "section": result.payload.get("section"),
                "doc_url": result.payload.get("doc_url"),
                "text": result.payload.get("text"),
            }
            results.append(result_data)
        return results
