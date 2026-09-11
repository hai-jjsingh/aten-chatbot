import os

from ollama import Client

from vectorstore.retriever import retrieve

ollama_client = Client(host=os.environ.get("OLLAMA_HOST", "http://localhost:11434"))


def retrieve_docs(state):

    question = state["question"]

    results = retrieve(question, limit=5)

    context = "\n\n".join(hit["entity"]["text"] for hit in results)

    return {
        "question": question,
        "context": context,
        "sources": [
            {
                "document_name": hit["entity"]["document_name"],
                "page_number": hit["entity"]["page_number"],
            }
            for hit in results
        ],
    }


NO_EVIDENCE_MESSAGE = "The query seems out of scope of the available documentation."


def generate_answer(state):

    # No relevant chunks survived the retrieval score threshold - skip the LLM
    # call entirely rather than asking it to "ground" an answer in nothing.
    if not state["context"].strip():
        return {**state, "answer": NO_EVIDENCE_MESSAGE}

    prompt = f"""You are a Command360 documentation assistant.

Rules:
1. Only answer using the supplied documentation.
2. Do not invent steps.
3. If insufficient evidence exists, say:
   "{NO_EVIDENCE_MESSAGE}"
4. Prefer procedural steps when available.

Context:
{state['context']}

Question:
{state['question']}
"""

    response = ollama_client.generate(model="qwen2.5:7b", prompt=prompt)

    answer = response.response

    return {**state, "answer": answer}
