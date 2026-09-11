from pymilvus import MilvusClient

client = MilvusClient(
    uri="http://localhost:19530"
)

collection_name = "command360_docs"

if client.has_collection(collection_name):
    client.drop_collection(collection_name)

client.create_collection(
    collection_name=collection_name,
    dimension=768
)

print(f"Collection '{collection_name}' created ✅")