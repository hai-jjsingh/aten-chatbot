from ollama import Client
from pymilvus import MilvusClient

COLLECTION = "command360_docs"

ollama_client = Client(
    host="http://localhost:11434"
)

milvus_client = MilvusClient(
    uri="http://localhost:19530"
)


def retrieve(query: str, limit: int = 5):

    query_embedding = ollama_client.embed(
        model="nomic-embed-text",
        input=query
    ).embeddings[0]

    milvus_client.load_collection(collection_name=COLLECTION)

    results = milvus_client.search(
        collection_name=COLLECTION,
        data=[query_embedding],
        limit=limit,
        output_fields=[
            "title",
            "source",
            "chunk_id",
            "text"
        ]
    )

    return results[0]