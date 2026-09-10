from ollama import Client
from pymilvus import MilvusClient

COLLECTION = "command360_docs"

ollama_client = Client(host="http://localhost:11434")

milvus_client = MilvusClient(uri="http://localhost:19530")

# Loaded once at import; Milvus keeps a loaded collection in memory across queries.
milvus_client.load_collection(collection_name=COLLECTION)


def retrieve(query: str, limit: int = 5):

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
