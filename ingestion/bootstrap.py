import os
import time

from ollama import Client
from pymilvus import MilvusClient

from vectorstore.schema import COLLECTION, ensure_collection

OLLAMA_HOST = os.environ.get("OLLAMA_HOST", "http://localhost:11434")
MILVUS_URI = os.environ.get("MILVUS_URI", "http://localhost:19530")

EMBED_MODEL = "nomic-embed-text"
LLM_MODEL = "qwen2.5:7b"

WAIT_TIMEOUT = int(os.environ.get("BOOTSTRAP_WAIT_TIMEOUT", "180"))
WAIT_INTERVAL = 3


def wait_for_ollama(client: Client):

    print("Waiting for Ollama...")

    deadline = time.monotonic() + WAIT_TIMEOUT

    while time.monotonic() < deadline:
        try:
            client.list()
            print("Ollama is ready")
            return
        except Exception:
            time.sleep(WAIT_INTERVAL)

    raise RuntimeError("Timed out waiting for Ollama to become available")


def wait_for_milvus(client: MilvusClient):

    print("Waiting for Milvus...")

    deadline = time.monotonic() + WAIT_TIMEOUT

    while time.monotonic() < deadline:
        try:
            client.list_collections()
            print("Milvus is ready")
            return
        except Exception:
            time.sleep(WAIT_INTERVAL)

    raise RuntimeError("Timed out waiting for Milvus to become available")


def ensure_models(client: Client):

    installed = {model.model for model in client.list().models}

    for model in (EMBED_MODEL, LLM_MODEL):

        if any(name == model or name.startswith(f"{model}:") for name in installed):
            print(f"Model already present: {model}")
            continue

        print(f"Pulling model: {model}...")
        client.pull(model)
        print(f"Pulled model: {model}")


def needs_indexing(created_collection: bool) -> bool:

    # Collection row-count stats can lag right after writes (unflushed segments,
    # soft-deleted upsert rows), so use collection existence as the signal instead.
    return created_collection


def bootstrap():

    ollama_client = Client(host=OLLAMA_HOST)
    milvus_client = MilvusClient(uri=MILVUS_URI)

    wait_for_ollama(ollama_client)
    wait_for_milvus(milvus_client)

    ensure_models(ollama_client)
    created_collection = ensure_collection(milvus_client)

    milvus_client.load_collection(collection_name=COLLECTION)

    if needs_indexing(created_collection):
        print("Collection is new, running ingestion pipeline...")
        from ingestion.index_documents import index_documents

        index_documents()
    else:
        print("Collection already exists, skipping ingestion")


if __name__ == "__main__":
    bootstrap()
