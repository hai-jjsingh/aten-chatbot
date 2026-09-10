from ollama import Client

from vectorstore.retriever import retrieve

ollama_client = Client(host="http://localhost:11434")


def retrieve_docs(state):

    question = state["question"]

    results = retrieve(question, limit=5)

    context = "\n\n".join(hit["entity"]["text"] for hit in results)

    return {
        "question": question,
        "context": context,
        "sources": [
            {
                "title": hit["entity"]["title"],
                "source": hit["entity"]["source"],
                "chunk_id": hit["entity"]["chunk_id"],
            }
            for hit in results
        ],
    }


def generate_answer(state):

    prompt = f"""
    You are a Command360 documentation assistant.

    Rules:
    1. Only answer from the supplied context.
    2. Do not invent steps.
    3. If evidence is missing say:
    "I could not find evidence in the Command360 documentation."
    4. At the end list the document titles used.

    Context:
    {state['context']}

    Question:
    {state['question']}
    """

    response = ollama_client.generate(model="qwen2.5:7b", prompt=prompt)

    answer = response.response

    return {**state, "answer": answer}
