import hashlib
import os

from ollama import Client
from pymilvus import MilvusClient

from ingestion.pdf_loader import load_pdf_pages
from ingestion.pdf_chunker import chunk_pages

COLLECTION = "command360_docs"
PDF_PATH = os.environ.get("PDF_PATH", "documents/confluence/Command360_User_Guide.pdf")

ollama_client = Client(host=os.environ.get("OLLAMA_HOST", "http://localhost:11434"))

milvus_client = MilvusClient(uri=os.environ.get("MILVUS_URI", "http://localhost:19530"))


def make_id(document_name: str, page_number: int, chunk_id: str) -> int:

    key = f"{document_name}*{page_number}*{chunk_id}"

    digest = hashlib.md5(key.encode()).hexdigest()

    # truncate to 63 bits so it fits INT64
    return int(digest[:16], 16) & 0x7FFFFFFFFFFFFFFF


def index_documents():

    print("Loading PDF pages...")

    pages = load_pdf_pages(PDF_PATH)

    print(f"Loaded {len(pages)} pages")

    chunks = chunk_pages(pages)

    print(f"Created {len(chunks)} chunks")

    data = []

    for idx, chunk in enumerate(chunks, start=1):

        embedding = ollama_client.embed(
            model="nomic-embed-text", input=chunk["text"]
        ).embeddings[0]

        data.append(
            {
                "id": make_id(
                    chunk["document_name"], chunk["page_number"], chunk["chunk_id"]
                ),
                "vector": embedding,
                "document_name": chunk["document_name"],
                "page_number": chunk["page_number"],
                "chunk_id": chunk["chunk_id"],
                "text": chunk["text"],
            }
        )

        print(f"Embedded chunk {idx}/{len(chunks)}")

    # upsert keeps reindexing idempotent since chunk ids are deterministic
    result = milvus_client.upsert(collection_name=COLLECTION, data=data)

    print(f"Indexed {len(data)} chunks, result: {result}")


if __name__ == "__main__":
    index_documents()
