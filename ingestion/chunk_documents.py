from langchain_text_splitters import (
    RecursiveCharacterTextSplitter
)


def chunk_documents(documents):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    chunks = []

    chunk_id = 1

    for document in documents:

        splits = splitter.split_text(
            document["content"]
        )

        for split in splits:

            chunks.append(
                {
                    "chunk_id": str(chunk_id),
                    "title": document["title"],
                    "source": document["source"],
                    "text": split
                }
            )

            chunk_id += 1

    return chunks