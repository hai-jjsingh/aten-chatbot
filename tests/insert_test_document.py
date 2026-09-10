from ollama import Client
from pymilvus import MilvusClient

COLLECTION = "command360_docs"

text = """
How to update an expired Certificate for Command360 using the recommended way?
Although, there are several ways to update a SSL/TLS certificate, but the recommended and most secure approach is to generate a Certificate Signing Request (CSR) directly from Command360. Generating the CSR within Command360 ensures that the private key never leaves the server, reducing the risk of exposure. The CSR can then be submitted to a Certificate Authority (CA) whether third-party, private, internal, or self-signed to obtain a valid certificate that matches the key pair held by Command360.

For the resulting certificate to function properly in a secure TLS handshake, both servers and clients must trust the CA that issued the certificate in the first place. When the certificate comes from a private, internal, or self-signed CA, trust is not established automatically. In these cases, the root and any intermediate certificates must be installed in the appropriate trust stores on Command360 servers to complete the certificate chain. Without this chain of trust, the handshake will fail, even if the certificate itself is valid and will most likely result in a 502.3 Bad Gateway HTTP Error rendering Command360 inaccessible.

Certificate Update Process Overview
Generate CSR in Command360.

Submit CSR to a CA (third-party, internal, private, or self-signed).

Receive signed certificate that matches the CSR public key.

Install signed certificate in Command360 binding it to the existing private key.

Upload or manually install CA root and any intermediate certificates.
"""

# Ollama
ollama_client = Client(host="http://localhost:11434")

embedding = ollama_client.embed(
    model="nomic-embed-text",
    input=text
).embeddings[0]

# Milvus
milvus_client = MilvusClient(
    uri="http://localhost:19530"
)

result = milvus_client.insert(
    collection_name=COLLECTION,
    data=[
        {
            "id": 1,
            "vector": embedding,
            "text": text,
            "source": "test_doc",
            "title": "Update Certificate",
            "chunk_id": "1"
        }
    ]
)

print("✅ Inserted")
print(result)
