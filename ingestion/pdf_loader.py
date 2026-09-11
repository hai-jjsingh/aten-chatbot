from pathlib import Path
import pymupdf


def load_pdf_pages(pdf_path: str):

    pdf = pymupdf.open(pdf_path)

    pages = []

    document_name = Path(pdf_path).stem

    for page_num in range(len(pdf)):

        page = pdf[page_num]

        text = page.get_text()

        if not text.strip():
            continue

        pages.append(
            {
                "document_name": document_name,
                "page_number": page_num + 1,
                "content": text,
            }
        )

    return pages
