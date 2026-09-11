from vectorstore.retriever import retrieve

results = retrieve("How do I update an expired certificate?")

for i, hit in enumerate(results, start=1):

    print("\n===================")
    print(f"Hit #{i}")
    print("===================")

    print(f"Score: {hit['distance']}")

    print(f"{hit['entity']['document_name']} " f"Page {hit['entity']['page_number']}")

    print(f"Chunk: {hit['entity']['chunk_id']}")

    print(hit["entity"]["text"][:300])
