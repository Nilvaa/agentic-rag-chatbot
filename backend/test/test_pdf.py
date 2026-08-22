from app.services.pdf_service import extract_text_from_pdf

file_path="uploads/documents/4b70efef-137d-42c4-97a9-4fff10231384_Apple-Human-Rights-Policy.pdf"

pages=extract_text_from_pdf(file_path)

print("Numbers of pages:",len(pages))

for page in pages[:2]:
    print("\n---Page",page["page_number"],"---")
    print(page["text"][:1000])