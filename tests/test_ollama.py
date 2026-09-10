from ollama import Client

client = Client(host="http://localhost:11434")

response = client.embed(
    model="nomic-embed-text",
    input="Command 360 device groups"
)

embedding = response["embeddings"][0]

print(f"Embedding dimensions: {len(embedding)}")
print(embedding[:5])