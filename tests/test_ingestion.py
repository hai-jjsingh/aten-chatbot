from ingestion.load_documents import (
    load_documents
)

from ingestion.chunk_documents import (
    chunk_documents
)

docs = load_documents(
    "documents/confluence"
)

chunks = chunk_documents(
    docs
)

print(f"Documents: {len(docs)}")
print(f"Chunks: {len(chunks)}")

print(chunks[0])