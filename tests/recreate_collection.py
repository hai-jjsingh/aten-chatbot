from pymilvus import MilvusClient

from vectorstore.schema import COLLECTION, create_command360_collection

client = MilvusClient(uri="http://localhost:19530")

if client.has_collection(COLLECTION):
    client.drop_collection(COLLECTION)

create_command360_collection(client)

print("command360_docs recreated")
