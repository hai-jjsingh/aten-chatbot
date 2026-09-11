from pymilvus import MilvusClient

client = MilvusClient(
    uri="http://localhost:19530"
)

stats = client.get_collection_stats(
    "command360_docs"
)

print(stats)