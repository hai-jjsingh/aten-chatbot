from langchain_text_splitters import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)


def chunk_pages(pages):

    chunks = []

    for page in pages:

        splits = splitter.split_text(page["content"])

        for index, split in enumerate(splits, start=1):

            chunks.append(
                {
                    "document_name": page["document_name"],
                    "page_number": page["page_number"],
                    "chunk_id": f"{page['page_number']}_{index}",
                    "text": split,
                }
            )

    return chunks
