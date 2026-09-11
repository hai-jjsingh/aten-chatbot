import os

from ollama import Client
from pymilvus import MilvusClient

COLLECTION = "command360_docs"

ollama_client = Client(host=os.environ.get("OLLAMA_HOST", "http://localhost:11434"))

milvus_client = MilvusClient(uri=os.environ.get("MILVUS_URI", "http://localhost:19530"))

_collection_loaded = False


def retrieve(query: str, limit: int = 5):

    global _collection_loaded

    # Deferred to first use: at import time the collection may not exist yet
    # (e.g. app startup runs bootstrap/ingestion after this module is imported).
    if not _collection_loaded:
        milvus_client.load_collection(collection_name=COLLECTION)
        _collection_loaded = True

    query_embedding = ollama_client.embed(
        model="nomic-embed-text", input=query
    ).embeddings[0]

    results = milvus_client.search(
        collection_name=COLLECTION,
        data=[query_embedding],
        limit=limit,
        output_fields=["document_name", "page_number", "chunk_id", "text"],
    )

    return results[0]
