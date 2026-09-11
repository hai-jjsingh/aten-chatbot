from vectorstore.retriever import retrieve

results = retrieve(
    "How do I update an expired certificate?"
)

for i, hit in enumerate(results, start=1):

    print("\n===================")
    print(f"Hit #{i}")
    print("===================")

    print(
        f"Score: {hit['distance']}"
    )

    print(
        f"Title: {hit['entity']['title']}"
    )

    print(
        f"Chunk: {hit['entity']['chunk_id']}"
    )

    print(
        hit['entity']['text'][:300]
    )