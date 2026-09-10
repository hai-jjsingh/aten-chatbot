from graph.workflow import graph

result = graph.invoke({"question": "How do I update an expired certificate?"})

print("\n=== ANSWER ===\n")

print(result["answer"])

print("\n=== SOURCES ===\n")

for source in result["sources"]:

    print(source["document_name"], source["page_number"])
