from app.services.chunking_service import chunk_pages
from app.services.pdf_service import extract_text_from_pdf

file_path="uploads/documents/e6340a3a-cfa1-4bae-a32a-2253c14254c0_Business-Conduct-Policy.pdf"

pages=extract_text_from_pdf(file_path)

chunks=chunk_pages(pages)
print("Number of pages: ",len(pages))
print("Number of chunks: ",len(chunks))

for chunk in chunks:
    print("\n---")
    print("Page:", chunk["page_number"])
    print("Chunk:", chunk["chunk_index"])
    print("Length:", len(chunk["content"]))
    print("Content:", chunk["content"][:100])
  