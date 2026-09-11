from pymilvus import DataType, MilvusClient

COLLECTION = "command360_docs"


def create_command360_collection(client: MilvusClient):

    schema = client.create_schema(auto_id=False, enable_dynamic_field=False)

    schema.add_field(field_name="id", datatype=DataType.INT64, is_primary=True)
    schema.add_field(field_name="vector", datatype=DataType.FLOAT_VECTOR, dim=768)
    schema.add_field(
        field_name="document_name", datatype=DataType.VARCHAR, max_length=512
    )
    schema.add_field(field_name="page_number", datatype=DataType.INT64)
    schema.add_field(field_name="chunk_id", datatype=DataType.VARCHAR, max_length=128)
    schema.add_field(field_name="text", datatype=DataType.VARCHAR, max_length=65535)

    index_params = client.prepare_index_params()
    index_params.add_index(
        field_name="vector", index_type="AUTOINDEX", metric_type="COSINE"
    )

    client.create_collection(
        collection_name=COLLECTION, schema=schema, index_params=index_params
    )


def ensure_collection(client: MilvusClient) -> bool:
    """Create the collection if it doesn't already exist (non-destructive).

    Returns True if the collection was newly created, False if it already existed.
    """

    if client.has_collection(COLLECTION):
        return False

    create_command360_collection(client)
    return True
