from pathlib import Path

def load_documents(folder: str):
    docs = []

    for file in Path(folder).rglob("*"):
        if file.suffix.lower() not in [".txt", ".md"]:
            continue

        content = file.read_text(
            encoding="utf-8",
            errors="ignore"
        )

        docs.append(
            {
                "title": file.stem.replace("_", " ").replace("-", " ").title(),
                "source": str(file),
                "content": content
            }
        )

    return docs


if __name__ == "__main__":
    docs = load_documents(
        "documents/confluence"
    )

    print(f"Loaded {len(docs)} documents")

    for doc in docs[:3]:
        print(doc["title"])