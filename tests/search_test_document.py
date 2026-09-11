from ollama import Client
from pymilvus import MilvusClient

COLLECTION = "command360_docs"

query = "How do device groups work?"

# Embed query
ollama_client = Client(host="http://localhost:11434")

query_vector = ollama_client.embed(
    model="nomic-embed-text",
    input=query
).embeddings[0]

# Search
milvus_client = MilvusClient(
    uri="http://localhost:19530"
)

results = milvus_client.search(
    collection_name=COLLECTION,
    data=[query_vector],
    limit=3,
    output_fields=["text", "source", "title"]
)

print(results)