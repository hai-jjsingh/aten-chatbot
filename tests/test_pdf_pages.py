from ingestion.pdf_loader import load_pdf_pages

pages = load_pdf_pages("documents/confluence/Command360_User_Guide.pdf")

print(f"Pages loaded: {len(pages)}")

print()

print(pages[0].keys())

print()

print(pages[0]["content"][:500])
