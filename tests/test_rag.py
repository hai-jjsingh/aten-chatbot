from ollama import Client
from pymilvus import MilvusClient

COLLECTION = "command360_docs"

question = "How do I update an expired certificate in Command360?"

ollama_client = Client(host="http://localhost:11434")

# Generate query embedding
query_embedding = ollama_client.embed(
    model="nomic-embed-text",
    input=question
).embeddings[0]

# Search Milvus
milvus_client = MilvusClient(
    uri="http://localhost:19530"
)

results = milvus_client.search(
    collection_name=COLLECTION,
    data=[query_embedding],
    limit=3,
    output_fields=["text", "title", "source"]
)

context = "\n\n".join(
    hit["entity"]["text"]
    for hit in results[0]
)

prompt = f"""
You are a Command360 documentation assistant.

Answer ONLY using the provided context.

If the answer is not in the context, say:
"I could not find evidence in the Command360 documentation."

Context:
{context}

Question:
{question}
"""

response = ollama_client.generate(
    model="qwen2.5:7b",
    prompt=prompt,
)

print("\n=== ANSWER ===\n")
print(response.response)

print("\n=== SOURCES ===\n")
for hit in results[0]:
    print(hit["entity"]["title"])