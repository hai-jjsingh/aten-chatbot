from pymilvus import MilvusClient, DataType

client = MilvusClient(uri="http://localhost:19530")

collection_name = "command360_docs"

if client.has_collection(collection_name):
    client.drop_collection(collection_name)

schema = client.create_schema(auto_id=False, enable_dynamic_field=False)

schema.add_field(field_name="id", datatype=DataType.INT64, is_primary=True)

schema.add_field(field_name="vector", datatype=DataType.FLOAT_VECTOR, dim=768)

schema.add_field(field_name="document_name", datatype=DataType.VARCHAR, max_length=512)

schema.add_field(field_name="page_number", datatype=DataType.INT64)

schema.add_field(field_name="chunk_id", datatype=DataType.VARCHAR, max_length=128)

schema.add_field(field_name="text", datatype=DataType.VARCHAR, max_length=65535)

index_params = client.prepare_index_params()
index_params.add_index(
    field_name="vector", index_type="AUTOINDEX", metric_type="COSINE"
)

client.create_collection(
    collection_name=collection_name, schema=schema, index_params=index_params
)

print("✅ command360_docs recreated")
