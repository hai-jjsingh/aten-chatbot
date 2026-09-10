from pymilvus import MilvusClient

client = MilvusClient(
    uri="http://localhost:19530"
)

print(
    client.describe_collection(
        collection_name="command360_docs"
    )
)