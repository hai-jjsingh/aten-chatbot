from ollama import Client
from pymilvus import MilvusClient

from ingestion.load_documents import load_documents
from ingestion.chunk_documents import chunk_documents

COLLECTION = "command360_docs"

ollama_client = Client(
    host="http://localhost:11434"
)

milvus_client = MilvusClient(
    uri="http://localhost:19530"
)


def index_documents():

    print("Loading documents...")

    documents = load_documents(
        "documents/confluence"
    )

    print(f"Loaded {len(documents)} documents")

    chunks = chunk_documents(
        documents
    )

    print(f"Created {len(chunks)} chunks")

    data = []

    for idx, chunk in enumerate(chunks, start=1):

        embedding = ollama_client.embed(
            model="nomic-embed-text",
            input=chunk["text"]
        ).embeddings[0]

        data.append(
            {
                "id": idx,
                "vector": embedding,
                "title": chunk["title"],
                "source": chunk["source"],
                "chunk_id": chunk["chunk_id"],
                "text": chunk["text"]
            }
        )

        print(
            f"Embedded chunk {idx}/{len(chunks)}"
        )

        print(f"Prepared {len(data)} records")

        print("\nSample record:")
        print(data[0])

    result = milvus_client.insert(
        collection_name=COLLECTION,
        data=data
    )

    print(
        f"✅ Indexed {len(data)} chunks, result: {result}"
    )


if __name__ == "__main__":
    index_documents()